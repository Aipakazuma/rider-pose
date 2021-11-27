<template>
  <el-container>
    <el-header>Header</el-header>
    <el-container>
      <el-aside width="200px">
        <el-row>
          <el-col>
            <CameraSelect v-on:connectLocalCamera="connectLocalCamera" />
          </el-col>
        </el-row>
        <el-row>
          <el-col v-if="isPossibleRecord">
            <el-button type="primary" v-on:click="startRecording">
              録画する
            </el-button>
          </el-col>
          <el-col v-else>
            <el-button type="info" v-on:click="stopRecording"
              >録画を終了する</el-button
            >
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-button
              type="primary"
              v-if="isPossibleDownload"
              v-on:click="downloadVideo"
            >
              ダウンロードする
            </el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-button
              type="success"
              v-if="isPossibleDownload"
              v-on:click="postVideo"
            >
              サーバへ保存する
            </el-button>
          </el-col>
        </el-row>
      </el-aside>
      <el-main>
        <video
          v-bind:srcObject.prop="stream"
          muted="true"
          autoplay
          playsinline
        ></video>
      </el-main>
    </el-container>
  </el-container>
</template>

<style lang="scss">
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
</style>

<script>
import CameraSelect from "./CameraSelect.vue";
import axios from "axios";

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

      // clear
      this.recordedChunks = [];

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
    postVideo: function () {
      const blob = new Blob(this.recordedChunks, { type: "video/webm" });
      const url =
        "https://adrwly0e6a.execute-api.ap-northeast-1.amazonaws.com/AipaTest";
      axios
        .post(url, blob)
        .then(function (response) {
          console.log("success", response);
        })
        .catch(function (error) {
          console.log("errro", error);
        });
    },
  },
  computed: {
    isPossibleDownload: function () {
      return this.recordedChunks.length > 0 && this.isPossibleRecord;
    },
  },
};
</script>
