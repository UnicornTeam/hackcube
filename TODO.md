- 不同页面间的数据传递：
  - NFC获取到数据后，通知RF界面展示通知
  - NFC页面生命周期会不会被destroy?
  - 返回后如何展示最新数据？

- How axios deal with:
  - 400 BAD Request
  - 404 NOT FOUND
  - 304 NOT MODIFIED
  - 500 INTERNAL SERVER ERROR


- WIFI List 分页

- Improve axios resp handler of above's http status:
- Handle 304 NOT MODIFIED in INFO page.

```
Handling Errors

axios.get('/user/12345')
  .catch(function (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log(error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message);
    }
    console.log(error.config);
  });
You can define a custom HTTP status code error range using the validateStatus config option.

axios.get('/user/12345', {
  validateStatus: function (status) {
    return status < 500; // Reject only if the status code is greater than or equal to 500
  }
})
```
