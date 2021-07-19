from main import Item, put_data, get_one


def create_obj(item_id, username, email, phone=None):
    return Item(
        item_id=item_id,
        username=username,
        email=email,
        phone=phone
    )

def test_object_equal():
    item_id=10
    username="Anastasia"
    email="a@a.ru"
    assert put_data(item_id, username, email) == Item(
        item_id=item_id,
        username=username,
        email=email
    )

def test_obj_saved():
    item_id=11
    username="Anastasiaa"
    email="a@b.ru"
    put_data(item_id, username, email)
    assert get_one(item_id=item_id)==Item(
        item_id=item_id,
        username=username,
        email=email
    )



