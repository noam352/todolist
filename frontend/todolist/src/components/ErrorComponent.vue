<template>
    <div class="error-message-container" v-if="errorMessage">
        <p class="error-message">{{ errorMessage }}</p>
    </div>
</template>

<script>
export default {
    props: {
        errorMessage: String // Error message passed from the parent component
    },
}
</script>

<style>
.error-message-container {
    display: block;
    text-align: center;
    /* Aligns the content of the container to the right */
}

.error-message {
    color: #dc3545;
    /* Red color for visibility */
    background-color: #ffeaea;
    /* Light background for contrast */
    border: 1px solid #dc3545;
    border-radius: 4px;
    /* Rounded corners */
    padding: 8px 10px;
    margin-top: 10px;
    /* Space above the message */
    font-size: 14px;
    line-height: 1.4;
    display: inline-block;
    /* Adjust the box to fit the content */
    text-align: left;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* Subtle shadow for depth */
}
</style>