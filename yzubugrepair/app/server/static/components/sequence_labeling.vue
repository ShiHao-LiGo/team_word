<!--
 * @Author: YaleXin
 * @Email: 181303209@yzu.edu.cn
-->
<!--
 * @Author: YaleXin
 * @Email: 181303209@yzu.edu.cn
-->
<template lang="pug">
extends ./annotation.pug

block annotation-area
  div.card
    header.card-header
      div.card-header-title.has-background-royalblue
        div.field.is-grouped.is-grouped-multiline
          div.control(v-for="label in labels")
            div.tags.has-addons
              a.tag.is-medium(
                v-shortkey.once="replaceNull(shortcutKey(label))"
                v-bind:style="{ \
                  color: label.text_color, \
                  backgroundColor: label.background_color \
                }"
                v-on:click="annotate(label.id)"
                v-on:shortkey="annotate(label.id)"
              ) {{ label.text }}
              span.tag.is-medium
                kbd {{ shortcutKey(label) | simpleShortcut }}
          div.control(v-for="rltsants in relationshipAnnotations[pageNumber]")
            span(
              v-bind:style="{ \
                  color: id2relationship[rltsants.relationship].text_color, \
                  backgroundColor: id2relationship[rltsants.relationship].background_color \
                }"
            )
              span {{id2annotationsText[rltsants.precursor_sequenceAnnotation]}}  
              span(style="color: #ff1111")  to 
              span {{id2annotationsText[rltsants.follow_sequenceAnnotation]}}
              span :
              span {{id2relationship[rltsants.relationship].text}}
              button.delete.is-small(v-on:click="removeRelationshipAnnotation(rltsants)") 
            
    div.card-content
      //- svg
      div.content.scrollable(v-if="docs[pageNumber] && annotations[pageNumber]", ref="textbox", id="canvas")
        annotator(
          v-bind:labels="labels"
          v-bind:relationships="relationships"
          v-bind:relationshipAnnotations="relationshipAnnotations[pageNumber]"
          v-bind:entity-positions="annotations[pageNumber]"
          v-bind:search-query="searchQuery"
          v-bind:text="docs[pageNumber].text"
          v-on:remove-label="removeLabel"
          v-on:add-label="addLabel"
          ref="annotator"
        )
      RelationshipDialog(
        v-bind:showEnable="DiglogShow"
        v-bind:pre_sequenceText="pre_sequenceText"
        v-bind:fowl_sequenceText="fowl_sequenceText"
        v-bind:relationships="relationships"
        v-on:closeDialog="closeRalationshipDialog"
        v-on:addRelationship="addRelationship"
      )
</template>

<style scoped>
.card-header-title {
  padding: 1.5rem;
}
</style>

<script>
import annotationMixin from './annotationMixin';
import Annotator from './annotator.vue';
import HTTP from './http';
import { simpleShortcut } from './filter';
//
import RelationshipDialog from './relationshipDialog.vue'
//
export default {
  filters: { simpleShortcut },

  // components: { Annotator },
  components: { Annotator: Annotator,  RelationshipDialog: RelationshipDialog},

  mixins: [annotationMixin],

  methods: {
    annotate(labelId) {
      this.$refs.annotator.addLabel(labelId);
    },


  

    addLabel(annotation) {
      console.log('sequence_labeling.vue : addLabel()')
      console.log('user add label');
      console.log('前端post之前：annotation = ')
      console.log(annotation)
      const docId = this.docs[this.pageNumber].id;
      HTTP.post(`docs/${docId}/annotations`, annotation).then((response) => {
        this.annotations[this.pageNumber].push(response.data);
      });
    },
    closeRalationshipDialog(){
      this.DiglogShow = false;
      console.log('closeRalationshipDialog()')
    },


  // 尝试添加关系
    tryAddRelationship(relationship, preSequenceText, fowlSequenceText) {
      this.newRelationshipAnnotaion = relationship;
      this.pre_sequenceText = preSequenceText;
      this.fowl_sequenceText = fowlSequenceText;
      console.log('参数：');
      console.log(relationship)
      console.log('user tries to  add relationship');
      console.log(this.annotations)
      const docId = this.docs[this.pageNumber].id;
      this.DiglogShow = true;
      // HTTP.post(`docs/${docId}/relationships-annotations`, relationship).then((response) => {
      //   this.relationshipAnnotations[this.pageNumber].push(response.data);
      //   // console.log(this.relationshipAnnotations)
      //   // console.log(response.data)
      // });
    },


// 添加关系
    addRelationship(relationshipId) {
      console.log('this.id2relationshipAnnotationIndex');
      console.log(this.id2relationshipAnnotationInde);
      console.log('要添加的关系Id：');
      console.log(relationshipId)
      this.newRelationshipAnnotaion.relationship = relationshipId;
      console.log('最终用户选择添加的关系类别是：');
      console.log(this.newRelationshipAnnotaion);
      const docId = this.docs[this.pageNumber].id;
      HTTP.post(`docs/${docId}/relationships-annotations`, this.newRelationshipAnnotaion).then((response) => {
        this.relationshipAnnotations[this.pageNumber].push(response.data);
        // console.log(this.relationshipAnnotations)
        // console.log(response.data)
      });
    },


    async submit() {
      const state = this.getState();
      this.url = `docs?q=${this.searchQuery}&seq_annotations__isnull=${state}&offset=${this.offset}&ordering=${this.ordering}`;
      await this.search();
      this.pageNumber = 0;
    },
  },

  computed: {
      id2annotationsText() {
        const text = this.docs[this.pageNumber].text;
        const id2annotationsText = {};
        // default value;
        for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
          const annotate = this.annotations[this.pageNumber][i];
          const annotationText = text.substring(annotate.start_offset, annotate.end_offset);
          id2annotationsText[annotate.id] = annotationText;
        }
        return id2annotationsText;
      },

      id2relationshipText() {
        const id2relationshipText = {};
        // default value;
        for (let i = 0; i < this.relationships.length; i++) {
          const relationship = this.relationships[i];
          id2relationshipText[relationship.id] = relationship.text;
        }
        return id2relationshipText;
      },

      id2relationship() {
        const id2relationship = {};
        // default value;
        for (let i = 0; i < this.relationships.length; i++) {
          const relationship = this.relationships[i];
          id2relationship[relationship.id] = relationship;
        }
        return id2relationship;
      },

      id2relationshipAnnotationIndex() {
        const id2relationshipAnnotationIndex = {};
        for (let i = 0; i < this.relationshipAnnotations[this.pageNumber].length; i++) {
          const relationshipAnnotation = this.relationshipAnnotations[this.pageNumber][i];
          id2relationshipAnnotationIndex[relationshipAnnotation.id] = i;
        }
        return id2relationshipAnnotationIndex;
      },

  },


};
</script>
