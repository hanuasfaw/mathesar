<script lang="ts">
  import type { Grouping, Group } from '@mathesar/stores/table-data/records';
  import { ROW_CONTROL_COLUMN_WIDTH } from '@mathesar/stores/table-data';
  import type { TableRecord } from '@mathesar/stores/table-data/types';
  import CellValue from '@mathesar/components/CellValue.svelte';

  export let row: TableRecord;
  export let grouping: Grouping;
  export let group: Group;
  export let rowWidth: number;

  $: ({ columnIds } = grouping);

  $: cellValue = (columnId: number) =>
    row.__groupValues ? row.__groupValues[columnId] : undefined;
</script>

<div
  class="cell row-control group-control"
  style="width:{ROW_CONTROL_COLUMN_WIDTH}px;left:0px"
/>

<div
  class="cell groupheader"
  style="left:{ROW_CONTROL_COLUMN_WIDTH}px;width:{rowWidth -
    ROW_CONTROL_COLUMN_WIDTH}px"
>
  {#each columnIds as columnId (columnId)}
    <span class="tag"
      >{columnId}: <CellValue value={cellValue(columnId)} /></span
    >
  {/each}
  <span class="tag count"><span class="label">count:</span> {group.count}</span>
</div>
