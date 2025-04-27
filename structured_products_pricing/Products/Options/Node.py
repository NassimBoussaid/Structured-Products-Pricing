from typing import Optional, Any
from math import exp

class Node:
    """
    Class to create and manage nodes used in Tree class.
    """
    def __init__(self, value: float, tree: Optional[Any], node_up: Optional[Any] = None, node_down: Optional[Any] = None):
        """
        Initializes Node.

        Parameters:
        - value: float. Asset price.
        - tree: Tree. Tree object is stored in each node that are part of it.
        - node_up: Optional[Node, None]. Node located above the current node.
        - node_down: Optional[Node, None]. Node located below the current node.
        """
        self.und_price: float = value
        self.layer: Optional[int] = None
        self.level: Optional[int] = None
        self.next_node_up: Optional[Node] = None
        self.next_node_mid: Optional[Node] = None
        self.next_node_down: Optional[Node] = None
        self.node_up: Optional[Node] = node_up
        self.node_down: Optional[Node] = node_down
        self.p_up: Optional[float] = None
        self.p_mid: Optional[float] = None
        self.p_down: Optional[float] = None
        self.p_cum: float = 0
        self.intrinsic_value: Optional[float] = None
        self.price: Optional[float] = None
        self.trunc: Optional[Node] = None
        self.node_behind: Optional[Node] = None
        self.tree = tree
        self.is_div_next_period: bool = False
        self.is_calculated: bool = False
        self.is_exercised: bool = False

    def add_node_up(self):
        """
        Creates an upper node, links it and sets its basic information.
        """
        self.node_up = Node(self.und_price * self.tree.alpha, node_down=self, tree=self.tree)
        self.node_up.layer = self.layer
        self.node_up.trunc = self.trunc
        self.node_up.level = self.level + 1

    def add_node_down(self):
        """
        Creates a lower node, links it and sets its basic information.
        """
        self.node_down = Node(self.und_price / self.tree.alpha, node_up=self, tree=self.tree)
        self.node_down.layer = self.layer
        self.node_down.trunc = self.trunc
        self.node_down.level = self.level - 1

    def add_node_mid(self):
        """
        Creates a middle node, links it and sets its basic information.
        """
        # Check if the dividend is paid in the next window
        self.is_div_next_period = not (self.are_same_dates(self.layer * self.tree.dt, self.tree.Market.time_to_div)) \
                               and (self.layer * self.tree.dt) < self.tree.Market.time_to_div \
                               and ((self.layer+1) * self.tree.dt > self.tree.Market.time_to_div
                                    or self.are_same_dates((self.layer+1) * self.tree.dt, self.tree.Market.time_to_div))
        # Create the next node mid based on the forward value
        self.next_node_mid = Node(self.forward_value(), tree=self.tree)
        self.next_node_mid.layer = self.layer + 1
        self.next_node_mid.level = self.level

    def add_probabilities(self):
        """
        Calculates the probabilities for a given node.
        """
        # Expected Value and Variance calculation
        Expected_Value: float = self.forward_value()
        Variance: float = (self.und_price ** 2 * exp(2 * self.tree.rates[self.layer] * self.tree.dt)
                           * (exp(self.tree.Market.vol**2 * self.tree.dt) - 1))
        # Probabilities calculation
        self.p_down = ((self.next_node_mid.und_price ** (-2) * (Variance + Expected_Value ** 2)
                       - 1 - (self.tree.alpha + 1) * (self.next_node_mid.und_price ** (-1) * Expected_Value - 1))
                       / ((1 - self.tree.alpha) * (self.tree.alpha ** (-2) - 1)))
        self.p_up = (self.next_node_mid.und_price ** (-1) * Expected_Value
                     - 1 - (self.tree.alpha ** (-1) - 1) * self.p_down) / (self.tree.alpha - 1)
        self.p_mid = 1 - self.p_up - self.p_down
        if self.p_down < 0 or self.p_up < 0 or self.p_mid < 0:
            print(f"Error: Negative probabilities at layer {self.layer} and level {self.level}")

    def add_probabilities_pruning(self):
        """
        Calculates the probabilities for a given node.
        """
        self.p_down = 0
        self.p_up = 0
        self.p_mid = 1

    def add_cum_probabilities(self):
        """
        Calculates the cumulative probabilities for a given node.
        """
        self.next_node_mid.p_cum += self.p_cum * self.p_mid
        if self.next_node_up is not None:
            self.next_node_up.p_cum += self.p_cum * self.p_up
        if self.next_node_down is not None:
            self.next_node_down.p_cum += self.p_cum * self.p_down

    def compute_intrinsic_value(self) -> float:
        """
        Calculates the intrinsic value for a given node.

        Returns:
        - self.intrinsic_value: float. The intrinsic value for a given node.
        """
        self.intrinsic_value = self.tree.Option.payoff(self.und_price)
        return self.intrinsic_value

    def compute_node_value(self):
        """
        Calculates the option value for a given node.
        """
        Discounted_Value: float = 0
        # Check if the next middle node exists
        if self.next_node_mid is not None:
            Discounted_Value = self.next_node_mid.price * self.p_mid
        # Check if the next upper node exists
        if self.next_node_up is not None:
            Discounted_Value += self.next_node_up.price * self.p_up
        # Check if the next lower node exists
        if self.next_node_down is not None:
            Discounted_Value += self.next_node_down.price * self.p_down
        # Discount the value
        Discounted_Value *= exp(-self.tree.rates[self.layer] * self.tree.dt)

        # Check if the option is european
        if self.tree.Option.option_name == "European":
            self.price = Discounted_Value
        # Check if the option is american
        elif self.tree.Option.option_name == "American":
            self.price = max(Discounted_Value, self.compute_intrinsic_value())
            if self.compute_intrinsic_value() > Discounted_Value:
                # Used for determining the exercise barrier
                self.is_exercised = True

    def is_next_node_mid(self, candidate_node: Optional[Any]) -> bool:
        """
        Checks whether the next middle node is the correct one based on forward value interval.

        Parameters:
        - candidate_node: Optional[Node]. The next middle node candidate.

        Returns:
        - bool. Determines whether the candidate node is within the valid interval.
        """
        return ((self.forward_value() < candidate_node.und_price * (1 + self.tree.alpha) / 2)
                and (self.forward_value() > candidate_node.und_price * (1 + self.tree.alpha) / (2 * self.tree.alpha)))

    def forward_value(self) -> float:
        """
        Calculates the forward value for a given node.

        Returns:
        - float. Forward value for a given node.
        """
        # Check if the dividend is paid in the next window and adapt the formula
        if self.trunc.is_div_next_period:
            return self.und_price * exp(self.tree.rates[self.layer] * self.tree.dt) - self.tree.Market.div_discrete
        else:
            return self.und_price * exp(self.tree.rates[self.layer] * self.tree.dt)

    def are_same_dates(self, d1: float, d2: float) -> bool:
        """
        Checks if two dates are the same (with a small margin of error).

        Parameters:
        - d1: float. First date.
        - d2: float. Second date.

        Returns:
        - bool. Determines whether the dates are same.
        """
        return abs(d1 - d2) < (1/365)/self.tree.nb_steps/10

    def pricing_cursed(self) -> float:
        """
        Computes the price of the option using Recursive pricing.

        Returns:
        - float. Option price.
        """
        # Check if the node has already been calculated
        if self.is_calculated:
            return self.price
        else:
            # Check if the node is a terminal node
            if self.next_node_mid is None:
                self.price = self.compute_intrinsic_value()
            else:
                # Initialize the price
                self.price = 0
                if self.next_node_mid is not None:
                    ValMid = self.next_node_mid.pricing_cursed()
                    self.price += ValMid * self.p_mid
                if self.next_node_up is not None:
                    ValUp = self.next_node_up.pricing_cursed()
                    self.price += ValUp * self.p_up
                if self.next_node_down is not None:
                    ValDown = self.next_node_down.pricing_cursed()
                    self.price += ValDown * self.p_down
                # Discount the price
                self.price *= exp(-self.tree.rates[self.layer] * self.tree.dt)
                # Check if the option is american
                if self.tree.Option.is_american():
                    self.price = max(self.price, self.compute_intrinsic_value())
            # Set the node as calculated
            self.is_calculated = True
            return self.price