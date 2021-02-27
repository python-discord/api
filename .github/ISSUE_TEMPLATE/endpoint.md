---
name: Endpoint/Route
about: Issues related to endpoints/routes
title: ''
labels: 'area: endpoint'
assignees: ''

---

# Description

# Reason

# New endpoints
<details>
  <summary>POST /api/v1/emojis/lemojis</summary>

### Description
New endpoint to register lemoji emojis in the database.
#### Request body
```json
{
    "name": "lemon_enraged",
    "id": 1234567890,
    "enabled": true
}
 ```

#### Response format
```json
{
    "pk": 12,
    "name": "lemon_enraged",
    "id": 1234567890,
    "enabled": true
}
 ```

#### Status codes
- 201: returned on success
- 400: if a given user is unknown or a field in the request body is invalid
</details>

# Changed endpoints
<details>
  <summary>GET /api/v1/emojis/duckies</summary>

### Description
The duckie endpoint has been modified: you can now query the duckies by name
#### Query params
- **name** `str`: filter the duckies by their name (accepts `*` wildcards)
- **id** `int`: filter the duckies by their snowflake id

Invalid query parameters will be ignored.

#### Response format
```json
[
    {
        "pk": 12,
        "name": "ducky_blurple",
        "id": 1234567890,
        "enabled": true
    },
    {
        "pk": 12,
        "name": "ducky_eivl",
        "id": 9080706050,
        "enabled": true
    }
]
 ```

#### Status codes
- 200: returned on success
</details>
