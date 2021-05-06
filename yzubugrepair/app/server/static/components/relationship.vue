<template lang="pug">
  div(v-cloak="")
    messages(v-bind:messages="messages")

    div.columns.is-multiline
      div.column.is-12
        a.button.is-primary(v-on:click="createRelatioship()") New relationship

      div.column.is-12(v-if="newRelatioship")
        div.box
          div.columns.is-multiline
            div.column.is-12
              div.tags.has-addons.mb0
                span.tag.is-medium(v-bind:style="{ \
                  color: newRelatioship.text_color, \
                  backgroundColor: newRelatioship.background_color \
                }") {{ newRelatioship.text }}

                //- span.tag.is-medium
                //-   kbd {{ shortcutKey(newRelatioship) | simpleShortcut }}

            div.column
              div.field
                relationship.relationship Relatioship name
                div.control
                  input.input(
                    type="text"
                    placeholder="Text input"
                    v-model="newRelatioship.text"
                  )

            div.column
              //- div.field
              //-   relationship.relationship Shortcut
              //-   div.field.has-addons
              //-     p.control
              //-       span.select
              //-         select(v-model="newRelatioship.prefix_key")
              //-           option(value="")
              //-           option(value="ctrl") Ctrl
              //-           option(value="shift") Shift
              //-           option(value="ctrl shift") Ctrl + Shift

              //-     div.control
              //-       div.select
              //-         select(v-model="newRelatioship.suffix_key")
              //-           option(disabled="", value="") key
              //-           option(v-for="ch in shortKeys", v-bind:key="ch") {{ ch }}

            div.column
              div.field
                relationship.relationship Color
                div.field.has-addons
                  div.control
                    div.form__field
                      div.form__input
                        swatches(
                          v-model="newRelatioship.background_color"
                          colors="basic"
                          show-fallback=true
                          popover-to=""
                          v-bind:trigger-style="{ width: '36px', height: '36px' }"
                        )
                  div.control
                    a.button.random-color-button(
                      v-on:click="setColor(newRelatioship)"
                    )
                      span.icon.is-small
                        i.fas.fa-sync-alt

            div.column
              div.field
                relationship.relationship &nbsp;
                div.field.is-grouped
                  p.control
                    a.button.is-light(v-on:click="cancelCreate()") Cancel

                  p.control
                    a.button.is-primary(v-on:click="addRelatioship()") Create relationship

    div.card
      header.card-header
        p.card-header-title {{ relationships.length }} relationships

        a.card-header-icon(href="#", aria-relationship="more options")
          span.icon
            i.fas.fa-angle-down(aria-hidden="true")

      div.card-content
        div.mb10(v-for="relationship in relationships", v-bind:key="relationship.id")
          div.level.is-mobile.mb0
            div.level-left
              div.level-item
                p.subtitle.is-5
                  div.tags.has-addons.mb0
                    span.tag.is-medium(v-bind:style="{ \
                      color: relationship.text_color, \
                      backgroundColor: relationship.background_color \
                    }") {{ relationship.text }}

                    //- span.tag.is-medium
                    //-   kbd {{ shortcutKey(relationship) | simpleShortcut }}

            div.level-right
              p.level-item
                div.field.is-grouped
                  p.control
                    a.button.is-text(v-on:click="editRelatioship(relationship)")
                      span.icon.is-small
                        i.fas.fa-pencil-alt
                      span Edit

                  p.control
                    a.button.is-text(v-on:click="removeRelatioship(relationship)")
                      span.icon.is-small
                        i.fas.fa-trash
                      span Delete

          div.columns(v-show="relationship === editedRelatioship")
            div.column
              div.field
                relationship.relationship Relatioship name
                div.control
                  input.input(
                    type="text"
                    placeholder="Text input"
                    v-model="relationship.text"
                  )

            div.column
              //- div.field
              //-   relationship.relationship Shortcut
              //-   div.field.has-addons
              //-     p.control
              //-       span.select
              //-         select(v-model="relationship.prefix_key")
              //-           option(value="")
              //-           option(value="ctrl") Ctrl
              //-           option(value="shift") Shift
              //-           option(value="ctrl shift") Ctrl + Shift

              //-     div.control
              //-       div.select
              //-         select(v-model="relationship.suffix_key")
              //-           option(disabled="", value="") key
              //-           option(v-for="ch in shortKeys", v-bind:key="ch") {{ ch }}

            div.column
              div.field
                relationship.relationship Color
                div.field.has-addons
                  div.control
                    div.form__field
                      div.form__input
                        swatches(
                          v-model="relationship.background_color"
                          colors="basic"
                          show-fallback=true
                          popover-to=""
                          v-bind:trigger-style="{ width: '36px', height: '36px' }"
                        )
                  div.control
                    a.button.random-color-button(
                      v-on:click="setEditColor"
                    )
                      span.icon.is-small
                        i.fas.fa-sync-alt

            div.column
              div.field
                relationship.relationship &nbsp;
                div.field.is-grouped
                  p.control
                    a.button.is-light(v-on:click="cancelEdit(relationship)") Cancel

                  p.control
                    a.button.is-primary(v-on:click="doneEdit(relationship)") Save changes
</template>

<style scoped>
.random-color-button {
  height: 36px;
  width: 36px;
  background-color: transparent;
  color: #404040;
  border: none;
}
</style>

<script>
import Swatches from 'vue-swatches';
import 'vue-swatches/dist/vue-swatches.min.css';
import HTTP from './http';
import Messages from './messages.vue';
// import { simpleShortcut } from './filter';

export default {
  components: { Messages, Swatches },

  // filters: { simpleShortcut },

  data: () => ({
    relationships: [],
    newRelatioship: null,
    editedRelatioship: null,
    messages: [],
    shortKeys: 'abcdefghijklmnopqrstuvwxyz',
  }),

  created() {
    HTTP.get('relationships').then((response) => {
      this.relationships = response.data;
      this.sortRelatioships();
    });
  },

  methods: {
    generateColor() {
      const gencolor = Math.floor(Math.random() * 0xFFFFFF).toString(16);
      const randomColor = '#' + ('000000' + gencolor).slice(-6);
      return randomColor;
    },

    blackOrWhite(hexcolor) {
      const r = parseInt(hexcolor.substr(1, 2), 16);
      const g = parseInt(hexcolor.substr(3, 2), 16);
      const b = parseInt(hexcolor.substr(5, 2), 16);
      return ((((r * 299) + (g * 587) + (b * 114)) / 1000) < 128) ? '#ffffff' : '#000000';
    },

    setColor(relationship) {
      const bgColor = this.generateColor();
      const textColor = this.blackOrWhite(bgColor);
      relationship.background_color = bgColor;
      relationship.text_color = textColor;
    },

    setEditColor() {
      this.setColor(this.editedRelatioship);
    },

    // shortcutKey(relationship) {
    //   let shortcut = relationship.suffix_key;
    //   if (relationship.prefix_key) {
    //     shortcut = `${relationship.prefix_key} ${shortcut}`;
    //   }
    //   return shortcut;
    // },

    sortRelatioships() {
      return this.relationships.sort((a, b) => ((a.text < b.text) ? -1 : 1));
    },

    addRelatioship() {
      if (this.newRelatioship.prefix_key === '') {
        this.newRelatioship.prefix_key = null;
      }
      HTTP.post('relationships', this.newRelatioship)
        .then((response) => {
          this.cancelCreate();
          this.relationships.push(response.data);
          this.sortRelatioships();
          this.messages = [];
        })
        .catch((error) => {
          console.log(error); // eslint-disable-line no-console
          if (error.response.data.non_field_errors) {
            error.response.data.non_field_errors.forEach((msg) => {
              this.messages.push(msg);
            });
          } else {
            this.messages.push('You cannot use same relationship name or shortcut key.');
          }
        });
    },

    removeRelatioship(relationship) {
      const relationshipId = relationship.id;
      HTTP.delete(`relationships/${relationshipId}`).then(() => {
        const index = this.relationships.indexOf(relationship);
        this.relationships.splice(index, 1);
      });
    },

    createRelatioship() {
      this.newRelatioship = {
        text: '',
        prefix_key: null,
        suffix_key: null,
        background_color: '#209cee',
        text_color: '#ffffff',
      };
      this.setColor(this.newRelatioship);
    },

    cancelCreate() {
      this.newRelatioship = null;
    },

    editRelatioship(relationship) {
      this.beforeEditCache = Object.assign({}, relationship);
      this.editedRelatioship = relationship;
    },

    doneEdit(relationship) {
      if (!this.editedRelatioship) {
        return;
      }
      this.editedRelatioship = null;
      relationship.text = relationship.text.trim();
      if (!relationship.text) {
        this.removeRelatioship(relationship);
      }
      HTTP.patch(`relationships/${relationship.id}`, relationship)
        .then(() => {
          this.sortRelatioships();
          this.messages = [];
        })
        .catch((error) => {
          console.log(error); // eslint-disable-line no-console
          if (error.response.data.non_field_errors) {
            error.response.data.non_field_errors.forEach((msg) => {
              this.messages.push(msg);
            });
          } else {
            this.messages.push('You cannot use same relationship name or shortcut key.');
          }
        });
    },

    cancelEdit(relationship) {
      this.editedRelatioship = null;
      Object.assign(relationship, this.beforeEditCache);
    },
  },
};
</script>
