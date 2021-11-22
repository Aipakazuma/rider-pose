<template>
  <div>
    <CameraSelect v-on:connectLocalCamera="connectLocalCamera" />
    <video id="my-video" muted="true" width="500" autoplay playsinline></video>
  </div>
</template>

<script>
import CameraSelect from "./CameraSelect.vue";

export default {
  name: "Video",
  components: {
    CameraSelect,
  },
  methods: {
    connectLocalCamera: async function (stream) {
      document.getElementById("my-video").srcObject = stream;
    },
  },
};
</script>
