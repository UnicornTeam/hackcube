import axios from 'axios';

export default {
  fetchNFCData(cb, errorCb) {
    axios
      .get(`${process.env.BACKEND_HOST}/nfc_item`, {
        validateStatus(status) {
          return status < 400; // Reject only if the status code is greater than or equal to 400
        },
      })
      .then((response) => {
        const result = response.data;
        // todo: check if nothing change
        console.log(result);
        if (response.status === 304) {
          return;
        }
        cb([result[result.data_key]]);
        // this.items = [result[result.data_key]];
        // this.$Message.success('Detect new nfc data.');
      })
      .catch((err) => {
        // TODO: How to handler error return?
        console.log(err.response);
        errorCb('Fetch nfc data fail');
        // this.$Message.error('Fetch nfc data fail.');
      });
  },
};
