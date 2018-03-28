<template>
  <div>
    <nav>
      <b-nav full tabs>
        <b-nav-item to="/">WIFI</b-nav-item>
        <!--<b-nav-item to="bt">BT</b-nav-item>-->
        <b-nav-item to="nfc">NFC</b-nav-item>
        <b-nav-item to="rf">RF</b-nav-item>
        <b-nav-item to="hid">HID</b-nav-item>
        <b-nav-item to="info">INFO</b-nav-item>
      </b-nav>
    </nav>

    <div style="margin-top: 10px">
      <b-alert variant="warning"
               dismissible
               :show="showDismissibleAlert"
               @dismissed="showDismissibleAlert=false">
        <h4>Warning!</h4>
        <p>本设备仅限风险演示,请您注意自觉遵守相关法律法规.</p>
      </b-alert>
    </div>
  </div>
</template>

<script>
  // TODO: Dynamic change active status
  export default {
    name: 'cube-nav',
    data() {
      return {
        showDismissibleAlert: true,
        isActive: false,
      };
    },
  };
</script>

<style scoped>

</style>
