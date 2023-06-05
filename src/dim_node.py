# dim_node.py

class Dim_Node:
    
    def __init__(self, dim=None, lim_inf=None, lim_sup=None, r=None, m=None, offset=None, minus_k=None, prev=None, next=None) -> None:
        self.dim = dim
        
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup
        
        self.r = r
        self.m = m
        self.offset = offset
        self.minus_k = minus_k
        
        self.prev = prev
        self.next = next
        
        
    def set_values(self, dim=None, lim_inf=None, lim_sup=None, r=None, m=None, offset=None, minus_k=None, prev=None, next=None) -> None:
        self.dim     = dim     if dim     is not None else self.dim
        self.lim_inf = lim_inf if lim_inf is not None else self.lim_inf
        self.lim_sup = lim_sup if lim_sup is not None else self.lim_sup
        self.r       = r       if r       is not None else self.r
        self.m       = m       if m       is not None else self.m
        self.offset  = offset  if offset  is not None else self.offset
        self.minus_k = minus_k if minus_k is not None else self.minus_k
        self.prev    = prev    if prev    is not None else self.prev
        self.next    = next    if next    is not None else self.next

    def calc_r(self):
        prev_r = self.prev.r if self.dim>1 else 1
        r = prev_r * (self.lim_sup-self.lim_inf+1)
        return r   
    
    def calc_m(self, prev_m):
        m = prev_m/(self.lim_sup-self.lim_inf+1)
        return m
    
    def calc_offset(self, prev_offset=0):
        offset = prev_offset + self.lim_inf*self.m
        return offset
    
    
    def to_dict(self):
        return {
            "lim_inf": self.lim_inf,
            "lim_sup": self.lim_sup,
            "m": self.m,
            "minus_k": self.minus_k,
        }