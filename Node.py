class Node:
    def __init__(self, val=None, alpha=None, beta=None, parent=None, children=None):
        self.val = val
        self.alpha = alpha
        self.beta = beta
        self.children = children
        self.parent = parent

    # Getters
    def get_val(self):
        return self.val

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
