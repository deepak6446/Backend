```
const jsonData = JSON.parse(responseBody);

pm.test("To have status code 201", function() {
    pm.expect(pm.response.status).to.equal("Created")
})
// console.log(jsonData)
pm.test("To have required keys", function() {
    pm.expect(jsonData).to.have.property("activityType")
    pm.expect(jsonData).to.have.property("recommendationId")
    pm.expect(jsonData).to.have.property("isDeleted")
    pm.expect(jsonData).to.have.property("activityId")
    pm.expect(jsonData.activityId).not.null
    postman.setEnvironmentVariable("activity-id", jsonData.activityId);
})
```
