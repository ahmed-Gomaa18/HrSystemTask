
def user_info(user : object) -> dict :
    return {
        "user_id" : user.pk,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,

    }