from django.core.exceptions import ValidationError

from mptt.models import MPTTModel


def validate_max_children(tree: MPTTModel, max_children: int) -> None:
    """
    Validates that the parent node does not exceed the maximum number of children.

    Parameters
    ----------
    tree
    max_children

    Returns
    -------

    """
    if tree.parent and tree.parent.max_children is not None:
        siblings = tree.parent.get_children().exclude(pk=tree.pk)
        if siblings.count() >= tree.parent.max_children:
            raise ValidationError(
                f"The parent node '{tree.parent}' cannot have more than {tree.parent.max_children} children.")

def validate_not_descendant_of_self(tree: MPTTModel) -> None:
    """
    Validates that the child node does not have one of its descendants as a parent.

    Parameters
    ----------
    tree: mptt.models.MPTTModel

    Returns
    -------

    """
    if tree.pk and tree.parent and tree.parent in tree.get_descendants():
            raise ValidationError("You cannot assign one of your own offspring as a parent.")

def validate_not_parent_of_self(tree: MPTTModel) -> None:
    """
    Validates that the node is not its own parent.

    Parameters
    ----------
    tree: mptt.models.MPTTModel

    Returns
    -------

    """
    if tree.pk and tree.parent and tree.parent.pk == tree.pk:
        raise ValidationError("A node cannot be a parent of itself.")