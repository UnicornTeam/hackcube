# Release 2018.4.4 Note:
- [RF]增加AttackUI和相关逻辑;
- [WIFI]离开WiFi页面后再回来，可以看到之前扫描的结果;
- [WIFI]离开WiFi页面时，自动关闭WiFi扫描按钮，向后台发送；
- [WIFI]离开WiFi页面时，自动检测ap_list和sta_list所有激活状态的item, UI转为非激活状态并逐个向后台发送off指令
- [RF]修改表头和调整CSS，让表格不用左右滑动查看；
- [RF]RF通知点击"Read More"自动下滑到表格；
- [NFC]添加日志框并自动检测后台日志文件是否更新，及时渲染到前端；
- [TEST]初步添加测试代码
- [WIFI]ap_list和client list中, 对过长的字符串采取省略号处理
- [RF]对Sniffer列表中过长的字符串采取自动换行处理
# TODO:
- [RF]上下左右导航键UI及具体逻辑实现
- [TEST]添加更多自动测试代码



# Release 2018.4.3 Note:

- 在WIFI获取、等待固件更新日志、获取RF初始列表时添加过渡动画
- UI改为全英文，包括提示消息、表头、描述信息等
- 修复WIFI页面下拉抖动问题
- 修复导航栏的WIFI项一直为选中状态的问题
- WiFi Scan 按钮实现条件渲 染，分为Scan(蓝色)和Stop(红色)两种状态
- 解决INFO页面更新日志字体过浅的问题
- WIFI页面表格Pagination改为居中显示
- 改进错误提示信息
- 修改sta_list 中的not associate 为None




