<template>
  <div>
    <CameraSelect v-on:connectLocalCamera="connectLocalCamera" />
    <video
      v-bind:srcObject.prop="stream"
      muted="true"
      width="500"
      autoplay
      playsinline
    ></video>
    <div v-if="isPossibleRecord">
      <button v-on:click="startRecording">録画する</button>
    </div>
    <div v-else>
      <button v-on:click="stopRecording">録画を終了する</button>
    </div>
    <button v-if="isPossibleDownload" v-on:click="downloadVideo">
      ダウンロードする
    </button>
  </div>
</template>

<script>
import CameraSelect from "./CameraSelect.vue";

export default {
  name: "Video",
  components: {
    CameraSelect,
  },
  data() {
    return {
      mediaRecorder: null,
      recordedChunks: [],
      stream: undefined,
      isPossibleRecord: true,
    };
  },
  methods: {
    connectLocalCamera: async function (stream) {
      this.stream = stream;
    },
    startRecording: function () {
      // 録画機能の生成
      if (this.stream === undefined) {
        alert("videoがonになっていません.");
        return;
      }
      this.mediaRecorder = new MediaRecorder(this.stream, {
        mimeType: "video/webm; codecs=vp8",
      });

      // availableイベントでメディア記録を保持
      this.mediaRecorder.ondataavailable = (event) =>
        this.recordedChunks.push(event.data);

      // 録画開始
      this.mediaRecorder.start();

      console.log("MediaRecorder start");
      this.isPossibleRecord = !this.isPossibleRecord;
    },
    stopRecording: function () {
      this.mediaRecorder.stop();
      this.isPossibleRecord = !this.isPossibleRecord;
    },
    downloadVideo: function () {
      /* eslint-disable */
      debugger;
      /* eslint-enable */
      const blob = new Blob(this.recordedChunks, { type: "video/webm" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style = "display: none";
      a.href = url;
      a.download = "video.webm";
      a.click();
      window.URL.revokeObjectURL(url);

      console.log("Video download");
    },
  },
  computed: {
    isPossibleDownload: function () {
      return this.recordedChunks.length > 0 && this.isPossibleRecord;
    },
  },
};
</script>
