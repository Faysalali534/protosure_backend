# protosure_backend
| Operations      | Status |
| ----------- | ----------- |
| Fetch issues for a given Github repo by it’s URL and store the following metadata in DB: number, title, description, status, creation date.| Done      |
| Add comments to an issue. Create the comment in Github and store it in DB.| Done     |
| Data must be kept in sync using GitHub webhooks API| Done      |
| API endpoint to list issues and their comments stored in DB.Filter by status and creation date (exact) and Search by number, title, description and comment text.|Done      |
| API endpoint to update status, title and description of a specific issue. This should update both DB and Github. Disallow concurrent updates of the same issue.   | Done   |
| Status update in Github should happen asynchronously in Celery. | Done      |
| tests   |Done      |
|Add a DB constraint that issues with the words WIP or DRAFT in title can not be closed.| Done     |


> You can find postman collection in `protosure_backend/protosure/Github Interaction.postman_collection.json`

## Demo Video
[Demo video for protosure](https://drive.google.com/file/d/1rooL6F11zRvifDBq6rKBDbhpE20fu7wj/view?usp=sharing)
