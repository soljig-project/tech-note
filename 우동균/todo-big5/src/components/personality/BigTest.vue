<template>
<div>
  <v-container>
  <div v-for="q in questions" :key="q.id">
    <h3>{{q.content}}</h3>
    <v-radio-group v-model="q.point" column row>
      <v-radio label="전혀 아니다" value=1 ></v-radio>
      <v-radio label="별로 아니다" value=2 ></v-radio>
      <v-radio label="중간이다" value=3></v-radio>
      <v-radio label="약간 그렇다" value=4></v-radio>
      <v-radio label="매우 그렇다" value=5></v-radio>
    </v-radio-group>
    <hr>
    <br>
  </div>
  <br>
  <v-btn x-large color="success" dark @click="checkPoint()"> click me! </v-btn>
  </v-container>
</div>
  
</template>

<script>
  export default {
    name : 'BigTest',
    data(){
      return {
        servey : [], // 외향성, 신경성, 성실성, 친화성, 개방성 순서로
        questions : [
          {
            id:1,
            content:'Q1 : 모르는 사람에게 먼저말을 건다.',
            point:0,
          },
          {
            id:2,
            content:'Q2 : 다른 사람이 편안하고 행복한지 확인한다.',
            point:0,
          },
          {
            id:3,
            content:'Q3 : 그림, 글, 음악을 창작한다.',
            point:0,
          },
          {
            id:4,
            content:'Q4 : 모든 일을 사전에 준비한다.',
            point:0,
          },
          {
            id:5,
            content:'Q5 : 울적하거나 우울함을 느낀다.',
            point:0,
          },
          {
            id:6,
            content:'Q6 : 회식, 파티, 사교모임을 계획한다.',
            point:0,
          },
          {
            id:7,
            content:'Q7 : 사람들을 비난한다.',
            point:0,
          },
          {
            id:8,
            content:'Q8 : 철학적이거나 영적인 문제들을 생각한다.',
            point:0,
          },
          {
            id:9,
            content:'Q9 : 일이나 물건을 정리하지 않고 어지럽게 그냥 둔다.',
            point:0,
          },
          {
            id:10,
            content:'Q10 : 스트레스나 걱정을 느낀다.',
            point:0,
          },
          {
            id:11,
            content:'Q11 : 어려운 단어를 사용한다.',
            point:0,
          },
          {
            id:12,
            content:'Q12 : 타인의 감정에 공감한다.',
            point:0,
          },
          ],
      }
    },
    methods:{
      checkPoint: function(){
        for (var i = 0; i< this.questions.length;i++){
          if (this.questions[i].point == 0){
            alert('설문을 완료해주세요');
            break;
          }
          else if (i == this.questions.length-1 ){
            this.sumPoint();
          }
        }
      },
      sumPoint:function(){
        var point_list = []
        for (let i = 0; i<this.questions.length; i++){
          var p = Number(this.questions[i].point)
          if (i==6 || i == 8){
            p = 6 - this.questions[i].point
          }
          point_list.push(p)
        }
        this.servey.push(point_list[0]+point_list[5])
        this.servey.push(point_list[4]+point_list[9])
        this.servey.push(point_list[3]+point_list[8])
        this.servey.push(point_list[1]+point_list[6]+point_list[11])
        this.servey.push(point_list[2]+point_list[7]+point_list[10])
        console.log(this.servey)
        this.$emit('serveyComplete', this.servey)
        this.servey=[]
      }
    },

  }
</script>

<style>

</style>