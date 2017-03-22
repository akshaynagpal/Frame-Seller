def hateoas_constraints(mul_order, host, stage, path, orderid=None):
    host = host.strip().strip('/')
    stage = stage.strip().strip('/')
    path = path.strip().strip('/')
    if orderid is not None:
        if mul_order:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + "/" + path + "/" + str(orderid)}]
        else:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + "/" + path + "/"}]
    else:
        links = [{"rel": "orders.list", "href": "https://" + host + "/" + stage + "/" + path + "/" }]
    return links


def hateoas_product(producturl):
    return {"rel": "order.product", "href": producturl}

"""
def hateoas_user(userid, host, stage):
    return {"rel": "order.user", "href": "https://" + host + "/" + stage + "/user/" + userid}
"""
