<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube HID Manage</h1>
    <h3 class="text-center">Using Cube to simulate keyboard, mouse, HID and other devices</h3>
    <br/>
    <h5>Key to output:</h5>
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
            { Index: 0, Info: '29d172a6', Name: 'Lock screen', Run: false },
            { Index: 1, Info: 'd2f392f1', Name: 'Add User', Run: false },
            { Index: 2, Info: '9209993f', Name: 'ShellCode', Run: false },
          ],
        };
      },
      methods: {
        serialSend(parameter) {
          axios
            .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
            .then((response) => {
              const message = response.data.message;
              this.$Message.success(message);
            })
            .catch((err) => {
              if (err.response) {
                this.$Message.error(err.response.data.message);
              } else {
                this.$Message.error('Request fail');
              }
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
        onUploadSuccess() {
          this.$Message.success('Upload success');
        },
        onUploadFail() {
          this.$Message.error('Upload fail');
        },
      },
    };
</script>

<style scoped>

</style>
