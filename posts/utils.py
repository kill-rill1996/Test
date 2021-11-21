def get_children(qs_child):
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'user': comment.user.id,
            'text': comment.text,
            'date_pub': comment.date.strftime('%H:%m %Y.%m.%d'),
            'parent': comment.get_parent,
            'is_child': comment.is_child,
        }
        if comment.child_comment.exists():
            c['children'] = get_children(comment.child_comment.all())
        res.append(c)
    return res


def create_comments_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'user': comment.user.id,
            'text': comment.text,
            'date_pub': comment.date.strftime('%H:%m %Y.%m.%d'),
            'parent': comment.get_parent,
            'is_child': comment.is_child,
        }
        if comment.child_comment:
            c['children'] = get_children(comment.child_comment.all())
        if not comment.parent:
            res.append(c)
    return res