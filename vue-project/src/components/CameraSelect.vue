<template>
  <p>
    カメラ:
    <el-select v-model="selectedVideo" @change="onChange">
      <el-option disabled value="">Please select one</el-option>
      <el-option
        v-for="(video, key, index) in videos"
        v-bind:key="index"
        :value="video.value"
      >
        {{ video.text }}
      </el-option>
    </el-select>
  </p>
</template>

<script>
export default {
  setup() {},
  data: () => ({
    selectedVideo: "",
    videos: [],
  }),
  mounted: async function () {
    //デバイスへのアクセス
    await navigator.mediaDevices.getUserMedia({ audio: true, video: true });
    const deviceInfos = await navigator.mediaDevices.enumerateDevices();

    //カメラの情報を取得
    deviceInfos
      .filter((deviceInfo) => deviceInfo.kind === "videoinput")
      .map((video) =>
        this.videos.push({
          text: video.label || `Camera  ${this.videos.length - 1}`,
          value: video.deviceId,
        })
      );
  },
  methods: {
    onChange: function () {
      if (this.selectedVideo != "") this.connectLocalCamera();
    },
    connectLocalCamera: async function () {
      const constraints = {
        video: this.selectedVideo
          ? { deviceId: { exact: this.selectedVideo } }
          : false,
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      this.$emit("connectLocalCamera", stream);
    },
  },
};
</script>
