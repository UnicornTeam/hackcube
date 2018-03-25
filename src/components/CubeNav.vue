<template>
  <nav class="bg-transparent">
    <b-nav tabs>
      <b-nav-item active>WIFI</b-nav-item>
      <b-nav-item to="bt">BT</b-nav-item>
      <b-nav-item to="nfc">NFC</b-nav-item>
      <b-nav-item to="rf">RF</b-nav-item>
      <b-nav-item to="hid">HID</b-nav-item>
      <b-nav-item to="info">INFO</b-nav-item>
    </b-nav>
  </nav>
</template>

<script>
  // TODO: Dynamic change active status
  // Should it?
  export default {
    name: 'cube-nav',
  };
</script>

<style scoped>

</style>
