<template>
  <table class="table">
        <thead>
        <tr>
            <th>#</th>
            <th>Name</th>
            <th>Running</th>
            <th>Status</th>
            <th>Ports</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="v, idx in containers">
            <th>{{idx}}</th>
            <td>{{ v.name }}</td>
            <td>
              <i :class="{is_runnging: true, true: v.attrs.State.Running}"></i>
            </td>
            <td>{{v.attrs.State.Status}}</td>
          <td>
            <ul v-if="Object.keys(v.attrs.NetworkSettings.Ports).length">
              <li v-for="k1 in Object.keys(v.attrs.NetworkSettings.Ports)">
                <label class="badge bg-success">{{k1.split('/')[0]}}</label>
                <ul>
                  <li v-for="v2 in v.attrs.NetworkSettings.Ports[k1]">{{v2.HostPort}}</li>
                </ul>
                {{k}}
              </li>
            </ul>
          </td>
        </tr>
        </tbody>
    </table>
</template>

<script>
export default {
  data() {
    return {
      containers: [],
    };
  },
  mounted() {
    this.containers = 123;
    let socket = new WebSocket('ws://192.168.1.151:6789');

    socket.onopen = function () {
      socket.send(JSON.stringify({
        "GET": 'DATA',
      }));
    };


    socket.onmessage = (e) => {
      let msg = JSON.parse(e.data);
      console.log(msg);

      if (msg.action == 'update' && msg.type == 'containers_list') {
        this.containers = msg.data;
      }
    };
  }
};
</script>

<style>
.is_runnging {
  width: 20px;
  height: 20px;
  display: block;
  background: #F00;
}

.is_runnging.true {
  background: #198754;
}

</style>