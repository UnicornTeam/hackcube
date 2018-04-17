import router from '@/router';
import axios from 'axios';

export default {
  data() {
    return {
      latest_nfc_item: '',
      latest_crf_items: [],
      showNFCAlert: false,
    };
  },
  methods: {
    fetchNFCData() {
      axios
        .get(`${process.env.BACKEND_HOST}/nfc_item`, {
          validateStatus(status) {
            return status < 400;
          },
        })
        .then((response) => {
          const result = response.data;
          if (response.status === 304) {
            return;
          }
          this.latest_nfc_item = result[result.data_key];
          this.showNFCAlert = true;
          this.$Message.info(result.message);
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
    fetchCRFItems() {
      const api = 'crf';
      const that = this;
      axios
        .get(`${process.env.BACKEND_HOST}/rf_item/${api}`, {
          validateStatus(status) {
            return status < 400; // Reject only if the status code is greater than or equal to 400
          },
        })
        .then((response) => {
          const result = response.data;
          // todo: write test code
          if (response.status === 304) {
            return;
          }
          const dataKey = result.data_key;
          if (result[dataKey].length > 0) {
            that.$Message.success(result.message);
          }
          // todo: change as for item of them :display notice
          if (dataKey === 'crf_item') {
            that.latest_crf_items = result[dataKey];
          }
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
    clickNFC() {
      router.push({
        path: '/nfc',
        name: 'NFC',
        params: {
          latest_nfc_item: this.latest_nfc_item,
        },
      });
    },
    clickRF() {
      router.push({
        path: '/rf',
        name: 'RF',
        params: {
          latest_crf_items: this.latest_crf_items,
        },
      });
    },
  },
};
