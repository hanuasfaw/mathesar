<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import FormElement from './FormElement.svelte';
  import type { FormBuildConfiguration } from './types.d';

  const dispatch = createEventDispatcher();

  export let form: FormBuildConfiguration;

  function submit() {
    dispatch('submit');
    return false;
  }
</script>

<div class="form-builder">
  <form on:submit|preventDefault={submit}>
    <FormElement
      stores={form.stores}
      storeUsage={form.storeUsage}
      variables={form.variables}
      element={form.layout}
    />
  </form>
</div>
