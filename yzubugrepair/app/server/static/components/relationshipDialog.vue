<!--
 * @Author: YaleXin
 * @Email: 181303209@yzu.edu.cn
-->
<template>
<div v-if="showEnable" id="MyPopup.vue">
    <div class="mask"></div>
    <div class="myPopup">
        <div class="UIdialog_hd">
            <strong class="UIdialogTitle">
                <span>{{pre_sequenceText}}</span> 
                <span style="color: red"> to </span>
                <span>{{fowl_sequenceText}}</span> 
            </strong>
        </div>
        <div class="UIdialog_bd">
            <form id="form" v-for="relationship in relationships" :key="relationship.id">
                <input type="radio" v-model="choose" v-bind:value="relationship.id">{{relationship.text}}
                <!-- <input type="radio" v-model="choose" value="选项二">选项二
                <input type="radio" v-model="choose" value="选项三">选项三
                <input type="radio" v-model="choose" value="选项四">选项四 -->
            </form>
      </div>
      <div class="footer">
        <span  class="left" @click="cancel">取消</span>
        <span  class="right" @click="confirm">确定</span>
      </div>

            
        </div>
</div>


</template>


<script>
export default {
    name: 'RelationshipDialog',

    props: {
        pre_sequenceAnnotation: {
            type: Number,
            default: -1,
        },
        fol_sequenceAnnotation: {
            type: Number,
            default: -1,
        },
        relationshipId: {
            type: Number,
            default: -1,
        },
        showEnable: {
            type: Boolean,
            default: false,
        },
        relationships: {
            type: Array,
            default: () => [],
        },
        pre_sequenceText: {
            type: String,
            default: '',
        },
        fowl_sequenceText: {
            type: String,
            default: '',
        },
    },


  data: () => ({
    choose: '',
  }),
    
    methods: {
        confirm(){
            console.log(' ---- ' + this.choose + ' ---- ' )
            console.log('点击了确定');
            if (this.choose == null || this.choose == '')alert('请选择添加的关系');
            else {
                this.$emit('addRelationship', this.choose);
                this.$emit('closeDialog');
            }
        },
        cancel(){   
            console.log('点击了取消');
            this.$emit('closeDialog');
        },
    },
    
}
</script>

<style scoped>
.myPopup{
    position: fixed;
    z-index: 5000;
    width: 80%;
    max-width: 300px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #FFFFFF;
    text-align: center;
    border-radius: 8px;
    overflow: hidden;
}
.mask{
    position: fixed;
    z-index: 1000;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6)
}
.footer{
    position: relative;
    line-height: 48px;
    font-size: 18px;
    display: flex;
    border-top: 1px solid #D5D5D6;
}
.left{
    background-color: gray;
    width: 50%;
}
.right{
    width: 50%;
    background-color: cadetblue;
}
</style>