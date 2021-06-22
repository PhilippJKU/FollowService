# FollowService

SET-UP

    Aufruf in der Konsole:

docker run --publish=7474:7474 --publish=7687:7687 -e 'NEO4J_AUTH=neo4j/secret' neo4j:4.2.4

Docker Desktop öffnen und neo4j Datenbank im Browser öffnen
Passwort auf "secret" ändern

localhost:5001/create

Request: 

{
"name" : "Benjamin"
}

localhost:5001/follow

Request:

{
"name" : "Benjamin",
"followName": "Florian"
}

localhost:5001/unfollow

Request:

{
"name" : "Anna",
"unfollowName": "Lena"
}

localhost:5001/getfollowed

Request:

[
    {
        "FOLGT": {
            "name": "Toni"
        }
    },
    {
        "FOLGT": {
            "name": "Lena"
        }
    }
]
