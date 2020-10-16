```
const jsonData = JSON.parse(responseBody);

pm.test("To have status code 201", function() {
    pm.expect(pm.response.status).to.equal("Created")
})
// console.log(jsonData)
pm.test("To have required keys", function() {
    pm.expect(jsonData).to.have.property("key1")
    pm.expect(jsonData).to.have.property("key2")
    pm.expect(jsonData).to.have.property("key3")
    pm.expect(jsonData).to.have.property("key4")
    pm.expect(jsonData.key5).not.null
    postman.setEnvironmentVariable("key-id", jsonData.key5);
})
```
