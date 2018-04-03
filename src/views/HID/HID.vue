<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube HID Manage</h1>
    <h3 class="text-center">用Cube模拟成键盘、鼠标、HID等设备</h3>
    <br/>
    <h5>要输出的键值</h5>
    <b-form-input v-model="Key"
                  type="text"
                  placeholder="Key">
    </b-form-input>
    <br/>
    <div class="text-center">
      <Button type="ghost" icon="ios-cloud-upload-outline" @click="onClickSubmit">Submit</Button>
    </div>
    <br/><br/>


    <h5>Script</h5>
    <b-table :items="items" :fields="fields">
      <div slot="Run" slot-scope="data">
        <b-button size="sm" variant="primary" @click="onClick(data.index)">Run</b-button>
      </div>
    </b-table>
  </div>
</template>

<script>
    import CubeNav from '@/components/CubeNav';
    import axios from 'axios';

    export default {
      name: 'HID',
      components: {
        CubeNav,
      },
      data() {
        return {
          Key: null,
          uploadHost: process.env.UPLOAD_API,
          extraData: { type: 'HID-Script' },
          fields: ['Info', 'Name', 'Run'],
          items: [
            { Index: 0, Info: '29d172a6', Name: '锁屏', Run: false },
            { Index: 1, Info: 'd2f392f1', Name: '添加用户', Run: false },
            { Index: 2, Info: '9209993f', Name: 'ShellCode', Run: false },
          ],
        };
      },
      methods: {
        serialSend(parameter) {
          axios
            .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
            .then((response) => {
              const result = response.data;
              console.log(result);
              this.$Message.success('Execute success.');
            })
            .catch((err) => {
              console.log(err.response);
              this.$Message.error('Execute fail.');
            });
        },
        onClickSubmit() {
          if (this.Key) {
            this.serialSend(this.Key);
          } else {
            this.$Message.error('Please input Key before submit.');
          }
        },
        onClick(index) {
          console.log(index);
          switch (index) {
            case 0:
              this.serialSend('ha');
              break;
            case 1:
              this.serialSend('hb');
              break;
            case 2:
              // 暂时不管
              break;
            default:
              break;
          }
        },
        onUploadSuccess(response) {
          console.log(response);
          this.$Message.success('Upload success');
        },
        onUploadFail(err) {
          console.log(err);
          this.$Message.error('Upload fail');
        },
      },
    };
</script>

<style scoped>

</style>
