<script lang="ts">
  import Checkbox from '@mathesar-component-library-dir/checkbox/Checkbox.svelte';
  import type { DynamicInputInterfaceType } from './types.d';

  export let value = false;
  export let interfaceType: DynamicInputInterfaceType = 'checkbox';
</script>

{#if interfaceType === 'toggle'}
  <!--TODO: Add css to checkbox to show a toggle view -->
  Toggle not implemented yet
{:else}
  <Checkbox {...$$restProps} bind:checked={value} />
{/if}
