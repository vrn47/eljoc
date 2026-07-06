def eljoc_session(request):
    """
    Make El Joc session variables available in every template.
    These variables identify:
    - the registered user (PlayerDB)
    - the current player in the selected edition
    - the player email
    - the selected edition
    - the username shown in the navigation bar
    They are read from the Django session and injected automatically
    into every rendered template.
    """

    return {
        "eljocsession_playerdb_id":
            request.session.get("eljocsession_playerdb_id"),

        "eljocsession_player_id":
            request.session.get("eljocsession_player_id"),

        "eljocsession_player_email":
            request.session.get("eljocsession_player_email"),

        "eljocsession_edition_short":
            request.session.get("eljocsession_edition_short"),

        "eljocsession_edition_id":
            request.session.get("eljocsession_edition_id"),

        "eljocsession_edition_name":
            request.session.get("eljocsession_edition_name"),

        "eljocsession_username":
            request.session.get("eljocsession_username"),
    }