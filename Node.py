class Node:
    def __init__(self, col=None, val=None, alpha=None, beta=None, parent=None, children=None):
        self.col = col
        self.val = val
        self.alpha = alpha
        self.beta = beta
        self.parent = parent
        self.children = children if children is not None else []

    # Getters
    def get_val(self):
        return self.val

    def get_col(self):
        return self.col

    def get_alpha(self):
        return self.alpha

    def get_beta(self):
        return self.beta

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    # Setters
    def set_val(self, val):
        self.val = val

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_beta(self, beta):
        self.beta = beta

    def set_children(self, children):
        self.children = children

    def set_parent(self, parent):
        self.parent = parent

    def set_col(self, col):
        self.col = col

    def add_child(self, child):
        self.children.append(child)
