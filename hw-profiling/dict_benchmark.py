
from typing import Dict, List, Any
from random import sample
from operator import setitem, getitem


def init_dict1(k: List[str], v: List[Any]) -> Dict[str, Any]:
    """Create dictionary using loop"""
    
    assert len(k) == len(v)
    d = {}
    
    for i in range(len(k)):
        d[k[i]] = v[i]
        
    return d


def init_dict2(k: List[str], v: List[Any]) -> Dict[str, Any]:
    """Create dictionary using dict constructor"""
    
    assert len(k) == len(v)
    d = dict(zip(k, v))
    
    return d


def init_dict3(k: List[str], v: List[Any]) -> Dict[str, Any]:
    """Create dictionary using dict comprehasion"""
    
    assert len(k) == len(v)
    d = {key: value for key, value in zip(k, v)}
    
    return d


def init_dict4(k: List[str], v: List[Any]) -> Dict[str, Any]:
    """Create dictionary using operator.setitem function"""
    
    assert len(k) == len(v)
    d = {}
    for i in range(len(k)):
        setitem(d, k, v)
    
    return d    


def get_dict_value1(d: Dict[str, Any], k: str) -> Any:
    """Get dict value using get method"""
    
    return d.get(k)


def get_dict_value2(d: Dict[str, Any], k: str) -> Any:
    """Get dict value by index key"""
    
    if k in d:
        return d[k]
    else:
        return None
    
    
def get_dict_value3(d: Dict[str, Any], k: str) -> Any:
    """Get dict value using operator.getitem function"""
    
    try:
        return getitem(d, k)
    except KeyError:
        return None
    

def dict_benchmark():
    """Function for demonstration purposes"""
    
    demo_dict = init_dict1(range(1000), sample(range(1000), 1000))
    demo_dict2 = init_dict2(range(1000), sample(range(1000), 1000))
    demo_dict3 = init_dict3(range(1000), sample(range(1000), 1000))
    demo_dict4 = init_dict4(range(1000), sample(range(1000), 1000))
    
    existing_keys = list(range(500))
    missing_keys = list(range(1000, 1500))
    keys = existing_keys + missing_keys
    
    for k in keys:
        get_dict_value1(demo_dict, k)
    
    for k in keys:
        get_dict_value2(demo_dict, k)
        
    for k in keys:
        get_dict_value3(demo_dict, k)
