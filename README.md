# Discount Hub API (ShellHacks 2023)
This program interfaces with a PostgreSQL database with PostGIS to provide information about nearby student discounts. For ShellHacks 2023 this is deployed on GCP Cloud Run. The database is running in GCP CloudSQL. The program itself is an extremely simple Flask/Gunicorn server that responds to the following endpoints.

# Endpoints
## \[POST\] /register
Registers a new user in the database and returns the user ID.
### Arguments
`email` - Email of the user.
### Returns (JSON)
`id` - Numeric ID of the newly created user.
### Example
`/register?email=webbgamers@gmail.com`

Response (201/CREATED): `{"id": 3}`

## \[POST\] /discount
Adds a new discount location to the database and returns the ID of said discount. Also automatically creates a rating by the specified user upvoting the discount.
### Arguments
`user` - Email of the user adding the discount.
`loc` - Coordinates of where the discount is in the format of `latitude longitude`.
`t` - Title of the location providing the discount.
`desc` - Description of the discount. (OPTIONAL)
`req` - Requirements to get the discount. Currently `student` should the only value given to this argument.
`amnt` - Amount of the discount. Just a string so could be anything such as `-20%`, `-$5`, or `FREE`.
### Returns (JSON)
`id` - Numeric ID of the newly created discount.
### Example
`/discount?user=webbgamers@gmail.com&loc=25.9127655%20-80.1557999&t=ShellHacks&desc=Located%20in%20the%20FIU%20Kovens%20Center&req=student&amnt=FREE`

Response (201/CREATED): `{"id": 8}`

## \[GET\] /discount
Fetches information about a discount using the discount's numeric ID.
### Arguments
`id` - Numeric ID of the discount.
### Returns (JSON)
`id` - Numeric ID of the discount.
`user` - Email of the user adding the discount.
`loc` - Coordinates of where the discount is in the format of `latitude longitude`.
`t` - Title of the location providing the discount.
`desc` - Description of the discount. (OPTIONAL)
`req` - Requirements to get the discount. Currently `student` should the only value given to this argument.
`amnt` - Amount of the discount. Just a string so could be anything such as `-20%`, `-$5`, or `FREE`.
### Example
`/discount?id=10`

Response (200/OK): `{"amount":"FREE","description":"Located in the FIU Kovens Center","id":12,"location":"25.9127655 -80.1557999","requirement":"student","title":"ShellHacks"}`

## \[GET\] /nearby
Returns a list of nearby discounts and related information.
### Arguments
`loc` - Center coordinate of search radius.
`r` - Search radius in meters.
### Returns (JSON)
This returns a potentially empty array of objects with the following data:
`id` - Numeric ID of the discount.
`user` - Email of the user adding the discount.
`loc` - Coordinates of where the discount is in the format of `latitude longitude`.
`t` - Title of the location providing the discount.
`desc` - Description of the discount. (OPTIONAL)
`req` - Requirements to get the discount. Currently `student` should the only value given to this argument.
`amnt` - Amount of the discount. Just a string so could be anything such as `-20%`, `-$5`, or `FREE`.
### Example
`/nearby?loc=25.9107681%20-80.1418737&r=5000`

Response (200/OK): `[{"amount":"-30%","description":"Must show ID, only on Sundays","id":11,"location":"25.9127655 -80.1557999","requirement":"student","title":"La Birra Bar"},{"amount":"FREE","description":"Located in the FIU Kovens Center","id":12,"location":"25.9127655 -80.1557999","requirement":"student","title":"ShellHacks"}]`

## \[POST\] /rate
Submits a vote for or against a particular discount.
### Arguments
`user` - Email of the user rating the discount.
`did` - Numeric ID of the discount under review.
`fb` - Feedback of the rating. Just a string but should only be `good` or `bad`.
### Returns (JSON)
`id` - Numeric ID of the rating.
### Example
`/rate?user=webbgamers@gmail.com&did=5&fb=good`

Response (201/CREATED): `{"id":16}`

# Errors
There are several errors you may receive from this API. They have an associated HTTP status code and return a JSON response formatted as such: `{"error": Error message}`.
## Missing Argument (400/BAD_REQUEST)
This occurs if you do not provide all the necessary arguments to one of the endpoints.

`{"error":"Missing argument"}`

## Not Found (404/NOT_FOUND)
This occurs if you attempt to retrieve data on something that doesn't exist. An example would be using the `/discount` GET endpoint with an invalid ID.

`{"error":"Not found"}`

## Internal Error (500/INTERNAL_SERVER_ERROR)
As of now there is very little data vaildation so it is very easy to trigger this. Malformed data, references to IDs that do not exist, or some other problem could cause this. In the event of this occuring, any pending SQL transactions should be rolled back so no damage will be done (probably).

`{"error":"Internal error"}`
