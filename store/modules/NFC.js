import NFC from '../../api/NFC';

// initial state
const state = {
  items: [],
};

// getters
const getters = {
  allNFCItems: state => state.items,
};

// actions
const actions = {
  getAllNFCItems({ commit }) {
    NFC.fetchNFCData(
      (items) => {
        commit('setNFCItems', items);
      },
      (err) => {
        commit();
      });
  },
};

// mutations
const mutations = {
  setNFCItems(state, items) {
    state.items = items;
  },

  // decrementProductInventory(state, { id }) {
  //   const product = state.all.find(product => product.id === id);
  //   product.inventory--;
  // },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
