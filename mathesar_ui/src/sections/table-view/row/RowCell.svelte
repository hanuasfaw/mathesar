<script lang="ts">
  import { tick } from 'svelte';
  import {
    isCellActive,
    scrollBasedOnActiveCell,
  } from '@mathesar/stores/table-data';
  import type {
    ColumnPosition,
    TableRecord,
    Column,
    Display,
    RecordsData,
  } from '@mathesar/stores/table-data/types';
  import Cell from '@mathesar/components/cell/Cell.svelte';

  export let recordsData: RecordsData;
  export let display: Display;
  export let columnPosition: ColumnPosition | undefined = undefined;
  export let row: TableRecord;
  export let column: Column;
  export let value: unknown = undefined;

  $: ({ activeCell } = display);
  $: isActive = $activeCell && isCellActive($activeCell, row, column);
  $: isLoading = !row.__state || row.__state === 'loading';

  // TODO: Set individual cell states and errors in recordsData

  async function checkTypeAndScroll(type?: string) {
    if (type === 'moved') {
      await tick();
      scrollBasedOnActiveCell();
    }
  }

  async function moveThroughCells(
    event: CustomEvent<{ originalEvent: KeyboardEvent; key: string }>,
  ) {
    const { originalEvent, key } = event.detail;
    const type = display.handleKeyEventsOnActiveCell(key);
    if (type) {
      originalEvent.stopPropagation();
      originalEvent.preventDefault();

      await checkTypeAndScroll(type);
    }
  }

  async function valueUpdated(e: CustomEvent<{ value: unknown }>) {
    const newValue = e.detail.value;
    if (newValue !== value) {
      value = newValue;
      if (row.__isNew) {
        await recordsData.createOrUpdateRecord(row, column);
      } else {
        await recordsData.updateCell(row, column);
      }
    }
  }
</script>

<div
  class="cell editable-cell"
  class:is-active={isActive}
  class:is-pk={column.primary_key}
  style="
      width:{columnPosition?.width ?? 0}px;
      left:{columnPosition?.left ?? 0}px;
    "
>
  <Cell
    {column}
    {isActive}
    {value}
    state={isLoading ? 'loading' : 'ready'}
    on:movementKeyDown={moveThroughCells}
    on:activate={() => display.selectCell(row, column)}
    on:update={valueUpdated}
  />
</div>

<style lang="scss">
  .editable-cell.cell {
    user-select: none;
    background-color: #fff;

    &.is-active {
      z-index: 5;
      background: #fff !important;
      border: none;
      min-height: 100%;
      height: auto !important;
    }
  }
</style>
