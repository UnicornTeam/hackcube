- Store origin data when navigate to another page, and restore it when back to origin page.

DONE AP List、Client List初始化为空
DONE NFC Page 按钮关闭无操作
DONE RF Page 里的TPMS数字输入框太窄

Done [Check All]for const of obj NOT for const in obj
TODO: Request Fail 次数达到上限停止请求
TODO：切换页面时，发送停止指令再跳转走
TODO: WiFi页面切出后 再切回 恢复状态 检测WIFI 文件是否为空
TODO: RF 页面表头缩写
DONE: 添加动画
DONE: INFO Update log 字体颜色太浅
DONE: WIFI Scan条件渲染
DONE: RF RF通知点击下滑
DONE: 改为全英文
DONE: WIFI滑动抖动
DONE: 导航的UI改进
DONE: 进入RF页面时读取/root/serial_file/data/aRF_Keeloq_data 和 cRF_24l01_data全部内容来初始化表格
DONE: Pagination 居中
DONE: success => this.$message.info
DONE: Server add all_rf_item
DONE: 完善error消息客户端显示 后端记录

Done WIFI 和 Client List
  DONE 点击了下面任意按钮停止Scan
  DONE WIFI 信道默认显示6
Done Client List 动态渲染

- 不同页面间的数据传递：
  - NFC获取到数据后，通知RF界面展示通知
  - NFC页面生命周期会不会被destroy?
  - 返回后如何展示最新数据？
- 在RF页面监听NFC,点击携带数据跳转到NFC并渲染数据

- How axios deal with:
  - 400 BAD Request
  - 404 NOT FOUND
  - 304 NOT MODIFIED
  - 500 INTERNAL SERVER ERROR


- WIFI List 分页
- 测试能否正确处理INFO页面的304，增加其他页面的304处理逻辑

- Change all response parser correspond backend response api.NOTE: Use data-key to get data.

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


