<template>
  <el-container>
    <el-header>Header</el-header>
    <el-container>
      <el-aside width="200px">
        <CameraSelect v-on:connectLocalCamera="connectLocalCamera" />
        <div v-if="isPossibleRecord">
          <el-button type="primary" v-on:click="startRecording">
            録画する
          </el-button>
        </div>
        <div v-else>
          <el-button type="info" v-on:click="stopRecording"
            >録画を終了する</el-button
          >
        </div>
        <el-button
          type="primary"
          v-if="isPossibleDownload"
          v-on:click="downloadVideo"
        >
          ダウンロードする
        </el-button>
      </el-aside>
      <el-main>
        <video
          v-bind:srcObject.prop="stream"
          muted="true"
          width="500"
          autoplay
          playsinline
        ></video>
      </el-main>
    </el-container>
  </el-container>
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
