from structured_products_pricing.Products.Options.Node import Node
from structured_products_pricing.Parameters.ModelParams import ModelParams
from typing import Optional, List, Tuple
import plotly.graph_objects as go
from math import exp, sqrt
from structured_products_pricing.Products.Options.OptionPricerBase import OptionPricerBase

class OptionPricerTree(OptionPricerBase):
    """
    Class to compute option prices using Trinomial method.
    """
    def __init__(self, model_params: ModelParams):
        """
        Initializes Tree.

        Parameters:
        - model_params: ModelParams. Market, Option and Pricer parameters.
        """
        super().__init__(model_params)
        self.nb_steps: int = self.Pricer.nb_steps
        self.last_node: Optional[Node] = None
        self.edge: list = []
        self.graph_mode: bool = False
        self.div_dt: float = self.Market.time_to_div / self.nb_steps
        self.alpha: float = exp(self.Market.vol * sqrt(3 * self.dt))
        self.root: Node = Node(self.Market.und_price, tree=self)
        self.root.level = 0
        self.root.layer = 0

    def create_tree(self):
        """
        Creates Tree and sets its basic parameters.
        """
        # Setting the root node
        current_node = self.root
        current_node.layer = 0
        current_node.level = 0
        current_node.p_cum = 1
        current_node.trunc = current_node
        # First triplet linked to the root
        current_node: Node = self.build_triplets(prev_node=current_node, candidate_node=None, is_trunc=True)
        # Loop on the number of steps
        for i in range(1, self.nb_steps):
            # Next node in the trunc
            current_node = self.build_column(current_node.next_node_mid)
        # Saving the last node for price computing
        self.last_node = current_node.next_node_mid

    def build_column(self, prev_node: Node) -> Node:
        """
        Builds columns for a given trunc node.

        Parameters:
        - prev_node: Node. An untouched trunc node.

        Returns:
        - prev_node: Node. A trunc node with upper and lower columns.
        """
        # Building triplet linked to the trunc
        prev_node: Node = self.build_triplets(prev_node=prev_node, candidate_node=None, is_trunc=True)
        # Setting the candidate node
        new_node: Node = prev_node.next_node_mid
        # Upper and lower column starting from the trunc
        prev_node = self.build_lower_column(prev_node.node_down, candidate_node=new_node.node_down)
        prev_node = self.build_upper_column(prev_node.node_up, candidate_node=new_node.node_up)
        return prev_node

    def build_lower_column(self, prev_node: Node, candidate_node: Node) -> Node:
        """
        Builds the lower column part for a given trunc node.

        Parameters:
        - prev_node: Node. An untouched trunc node.
        - candidate_node: Node. The next node on the trunc.

        Returns:
        - prev_node: Node. A reworked trunc node for which lower column is filled.
        """
        # Loop for all existing node in the lower part
        while prev_node is not None:
            # Condition to check dividends
            if prev_node.trunc.is_div_next_period:
                # Special-case handling : Forward is negative
                if prev_node.forward_value() <= 0:
                    return prev_node.trunc
                # Loop to correctly reconnect nodes
                while not (prev_node.is_next_node_mid(candidate_node)):
                    # Creating a new node until we find the right one
                    candidate_node.add_node_down()
                    candidate_node = candidate_node.node_down
            # Building triplet linked to the current node
            prev_node = self.build_triplets(prev_node=prev_node, candidate_node=candidate_node, is_trunc=False)
            # Force exit if we are at the end of the column
            if prev_node.node_down is None:
                return prev_node.trunc
            # Moving to the next node
            prev_node = prev_node.node_down
            candidate_node = candidate_node.node_down
        return prev_node.trunc

    def build_upper_column(self, prev_node: Node, candidate_node: Node) -> Node:
        """
        Builds the upper column part for a given trunc node.

        Parameters:
        - prev_node: Node. An untouched trunc node.
        - candidate_node: Node. The next node on the trunc.

        Returns:
        - prev_node: Node. A reworked trunc node for which upper column is filled.
        """
        # Loop for all existing node in the lower part
        while prev_node is not None:
            # Condition to check dividends
            if prev_node.trunc.is_div_next_period:
                # Loop to correctly reconnect nodes
                while not (prev_node.is_next_node_mid(candidate_node)):
                    # Creating a new node until we find the right one
                    candidate_node.add_node_up()
                    candidate_node = candidate_node.node_up
            # Building triplet linked to the current node
            prev_node = self.build_triplets(prev_node=prev_node, candidate_node=candidate_node, is_trunc=False)
            # Force exit if we are at the end of the column
            if prev_node.node_up is None:
                return prev_node.trunc
            # Moving to the next node
            prev_node = prev_node.node_up
            candidate_node = candidate_node.node_up
        return prev_node.trunc

    def build_triplets(self, prev_node: Node, candidate_node: None, is_trunc: bool) -> Node:
        """
        Builds triplet for a given node.

        Parameters:
        - prev_node: Node. The current node.
        - candidate_node: Node. The node in front of the current one.
        - is_trunc: bool. Determines whether a node is on the trunc.

        Returns:
        - prev_node: Node. The current node reworked.
        """
        # Check if the candidate node is already set
        if candidate_node is None:
            prev_node.add_node_mid()
            candidate_node = prev_node.next_node_mid
        # Check if the candidate node is part of the trunc
        if is_trunc:
            candidate_node.trunc = candidate_node
            candidate_node.node_behind = prev_node
        # Set the next middle node and calculate probabilities
        prev_node.next_node_mid = candidate_node
        prev_node.add_probabilities()
        # Check pruning conditions and only create the next middle node if needed
        if ((prev_node.node_up is None and prev_node.p_cum * prev_node.p_up < self.Pricer.pruning_limit) or
                (prev_node.node_down is None and prev_node.p_cum * prev_node.p_down < self.Pricer.pruning_limit)):
            prev_node.add_probabilities_pruning()
        # Normal case
        else:
            if candidate_node.node_up is None:
                candidate_node.add_node_up()
            if candidate_node.node_down is None:
                candidate_node.add_node_down()
            # Link nodes
            prev_node.next_node_up = candidate_node.node_up
            prev_node.next_node_down = candidate_node.node_down
        # Add cumulated probabilities
        prev_node.add_cum_probabilities()
        # Save links between nodes for graphing
        if self.graph_mode:
            self.connect_nodes_graph(prev_node, candidate_node)
        return prev_node

    def connect_nodes_graph(self, prev_node: Node, candidate_node: Node):
        """
        Connect nodes for graphing.

        Parameters:
        - prev_node: Node. The current node.
        - candidate_node: Node. The node in front of the current one.
        """
        self.edge.append((prev_node, candidate_node))
        if prev_node.next_node_up is not None:
            self.edge.append((prev_node, candidate_node.node_up))
        if prev_node.next_node_down is not None:
            self.edge.append((prev_node, candidate_node.node_down))

    def compute_price(self) -> float:
        """
        Computes the price of the option using Backward pricing.

        Returns:
        - float. The option price.
        """
        current_node: Node = self.last_node
        prev_node: Node = current_node.node_behind
        # Add intrinsic value to the last column
        self.add_intrinsic_column(current_node)
        # Loop until we reach the root
        while prev_node is not None:
            # Compute the trunc option price
            prev_node.compute_node_value()
            # Loop to compute the option price for the upper part
            while prev_node.node_up is not None:
                prev_node = prev_node.node_up
                prev_node.compute_node_value()
            # Set back the node to the trunc
            prev_node = current_node.node_behind
            # Loop to compute the option price for the lower part
            while prev_node.node_down is not None:
                prev_node = prev_node.node_down
                prev_node.compute_node_value()
            # Exit if we reach the root
            if prev_node.trunc.node_behind is None:
                return prev_node.price
            # Move to the next node (node behind in fact)
            current_node = current_node.node_behind
            prev_node = current_node.node_behind
        return current_node.price

    @staticmethod
    def add_intrinsic_column(trunc_node: Node):
        """
        Computes intrinsic value for an entire column.

        Arguments:
        - trunc_node: Node. Node located on the trunc of the tree.
        """
        current_node: Node = trunc_node
        current_node.price = current_node.compute_intrinsic_value()
        # Loop to compute the intrinsic value for the upper part
        while current_node.node_up is not None:
            current_node = current_node.node_up
            current_node.price = current_node.compute_intrinsic_value()
        # Set back the node to the trunc
        current_node = trunc_node
        # Loop to compute the intrinsic value for the lower part
        while current_node.node_down is not None:
            current_node = current_node.node_down
            current_node.price = current_node.compute_intrinsic_value()

    def graph_tree(self):
        """
        Graphs tree using plotly.
        """
        # List for all existing nodes
        list_node, xe, ye = self.generate_nodes_and_links()
        # X and Y axis to represent nodes
        xn = [node.layer for node in list_node]
        yn = [node.und_price for node in list_node]
        info_list = []
        # Loop to create the information for each node
        for node in list_node:
            if node.p_mid is not None:
                info_list.append([f"price : {round(node.und_price, 2)}",
                                  f"P_Up : {round(node.p_up, 2)}",
                                  f"P_Mid : {round(node.p_mid, 2)}",
                                  f"P_Down : {round(node.p_down, 2)}",
                                  f"P_Cum : {round(node.p_cum, 7)}"])
            else:
                info_list.append([f"price : {round(node.und_price, 2)}",
                                  f"P_Up : {node.p_up}",
                                  f"P_Mid : {node.p_mid}",
                                  f"P_Down : {node.p_down}",
                                  f"P_Cum : {round(node.p_cum, 7)}"])
        node_scale = [max(10, 20 * node.p_cum) for node in list_node]
        node_color = ["#D096E4" if node.is_exercised else "#77B5CB" for node in list_node]
        fig = go.Figure()
        # Load graph for links
        fig.add_trace(go.Scattergl(x=xe, y=ye, mode='lines', name='Link',
                                   line=dict(color='rgb(210,210,210)', width=1), hoverinfo='none'))
        # Load graph for nodes
        fig.add_trace(go.Scatter(x=xn, y=yn, mode='markers+text', name='Node',
                                 marker=dict(symbol='circle-dot', size=node_scale, color=node_color,
                                             line=dict(color='rgb(50,50,50)', width=1)),
                                 opacity=0.8, hovertemplate=['<br>'.join(info) for info in info_list]))
        # Display graph
        fig.show()

    def generate_nodes_and_links(self) -> Tuple[List, List[float], List[float]]:
        """
        Generates the list of nodes and their links for the tree graph.

        Returns:
        - list_node: List of all nodes in the tree.
        - xe: X-axis coordinates for links between nodes.
        - ye: Y-axis coordinates for links between nodes.
        """
        list_node = []
        # X and Y axis to represent "links" between nodes
        xe, ye = [], []
        # Loop to create the list of nodes and links
        for node_1, node_2 in self.edge:
            xe += [node_1.layer, node_2.layer, None]
            ye += [node_1.und_price, node_2.und_price, None]
            if node_1 not in list_node:
                list_node.append(node_1)
            if node_2 not in list_node:
                list_node.append(node_2)
        return list_node, xe, ye