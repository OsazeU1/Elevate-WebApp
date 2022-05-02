# ENGO 551 - Final Project

### Elevate Web Application"# Elevate-WebApp-"

### API Documentation

The Elevate RESTful API only allows for GET requests of a user's habit information.

The /api/user/<userid> route will then select the top two habits and their corresponding streaks based on the inputted user ID.

```python
def apiuser(userid):
    username = session["user_name"]
    taken_q = "SELECT apikey FROM users WHERE username = '" + str(username) + "'"
    taken_temp = db.execute(taken_q).fetchone()
    print(taken_temp[0])
    if  taken_temp[0]== None:
        return jsonify({"error": "404 - Account does not have an APIkey."})

    result = db.execute("SELECT * FROM users WHERE userid = :userid", {
                        "userid": int(userid)}).fetchone()

    print(type(userid))
    # Check if user exists, in case user is typed in the address bar
    if result is None:
        return jsonify({"error": "404 - UserID is not in our database."}), 404

    user_result = db.execute("SELECT * FROM userhabits WHERE userid = :userid", {
                        "userid": userid}).fetchall()

    print(user_result)
    habitcat1 = user_result[0][2]
    cat1_streak = user_result[0][3]

    habitcat2 = user_result[1][2]
    cat2_streak = user_result[1][3]

    return jsonify({
        "Username": username,
        "Habit 1": habitcat1,
        "Habit 1 Streak": cat1_streak,
        "Habit 2": habitcat2,
        "Habit 2 Streak": cat2_streak
    })
```

If the user requesting the data does not have an API key, they will recieve the following message

```python
    if  taken_temp[0]== None:
        return jsonify({"error": "404 - Account does not have an APIkey."})

```

If no results were found the page would return an error message stating the user is not in our database and a 404 code.

```python
    # Check if user exists, in case user is typed in the address bar
    if result is None:
        return jsonify({"error": "404 - UserID is not in our database."}), 404

```

The function finally returns a JSON package of the parameters of interest.

```python
    return jsonify({
        "Username": username,
        "Habit 1": habitcat1,
        "Habit 1 Streak": cat1_streak,
        "Habit 2": habitcat2,
        "Habit 2 Streak": cat2_streak
    })
```

#### For example: The /api/user/2 request returns

```python

    {
        "Habit 1": "Eating",
        "Habit 1 Streak": 5,
        "Habit 2": "Fitness",
        "Habit 2 Streak": 20,
        "Username": "freshaccount2",
    })
```

The api/generate route displays the users API key.

```python
    return jsonify({
        "API Key": key,
        "username": username,
    })

```

It does this by checking if the user has an API key, if they don't it generates on for them and stores it in the database.

```python
def generate_hash_key():
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    username = session["user_name"]
    taken = False

    taken_q = "SELECT apikey FROM users WHERE username = '" + str(username) + "'"
    taken_temp = db.execute(taken_q).fetchone()
    print(taken_temp[0])
    if  taken_temp[0]!= None:
       taken = True

```

If the user has a key, this route requests the key and returns it.

```python
    if not taken:
        message = str(random.getrandbits(256)).encode()

        key = hashlib.sha256(message).hexdigest()
        db.execute("UPDATE users SET apikey = :key WHERE username = :username", {
            "key": key, "username":username})
        db.commit()
    else:
        print('in here')
        key = taken_temp[0]
```

#### For example, the api/generate route returns

```python
   {

        "username": 	"ac74461414d39af2f2cfa4ad2e1f82f3a6e016e39da77e716248d3fda8af7ec6",
        "API Key": "test1"
    })
```
