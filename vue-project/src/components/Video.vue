<template>
  <div>
    <p>
      カメラ:
      <select v-model="selectedVideo" @change="onChange">
        <option disabled value="">Please select one</option>
        <option
          v-for="(video, key, index) in videos"
          v-bind:key="index"
          :value="video.value"
        >
          {{ video.text }}
        </option>
      </select>
    </p>
    <video id="my-video" muted="true" width="500" autoplay playsinline></video>
  </div>
</template>

<script>
export default {
  name: "Video",
  data: () => ({
    videos: [],
    selectedVideo: "", //追記
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
      document.getElementById("my-video").srcObject = stream;
    },
  },
};
</script>
