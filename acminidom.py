from xml.dom.minidom import parse

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def attributesOf(aNode):
        def helper():
                attrs = aNode.attributes
                l = attrs.length
                for i in range(l):
                        attr = attrs.item(i)
                        yield (str(attr.localName),attr.value)
        return dict(helper())

