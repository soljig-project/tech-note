<template>
  <div class="">
    <h1> Big 5 test </h1>
    <p>https://m.blog.naver.com/PostView.nhn?blogId=zzai84&logNo=220975340451&proxyReferer=https:%2F%2Fwww.google.com%2F</p>
    <big-test @serveyComplete=showChart></big-test>
  </div>
</template>

<script>
  // import HelloWorld from './components/HelloWorld';
  import BigTest from './components/personality/BigTest.vue';

  export default {
    name: 'App',
    components: {
      BigTest,
    },
    methods:{
      showChart(servey){
        console.log('app vue'+servey)
      },
    }
  };
</script>