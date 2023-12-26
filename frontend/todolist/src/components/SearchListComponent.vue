<template>
    <div>
        <button class="button" v-if="!showForm" @click="showForm = true">Search For List</button>
        <div v-else>
            <input class="input-field" v-model="listName" placeholder="Enter list name">
            <button class="button" :disabled="!listName.trim()" @click="submitList">Submit</button>
            <!-- Display error message if it exists (from prop) -->
        </div>
    </div>
</template>
  
<script>
export default {
    // props: {
    //     errorMessage: String // Error message passed from the parent component
    // },
    data() {
        return {
            showForm: false,
            listName: ''
        };
    },
    methods: {
        submitList() {
            if (this.listName.trim()) {
                this.$emit('list-search', this.listName);
                this.showForm = false;
                this.listName = '';
                // Do not reset the errorMessage here; let the parent handle it
            }
        }
    }
};
</script>
  
<style></style>