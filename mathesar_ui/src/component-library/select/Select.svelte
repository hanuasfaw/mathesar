<!--
  @component

  **NOTICE** This component will eventually be redesigned, with its props
  behaving more like `SimpleSelect`.

  https://github.com/centerofci/mathesar/issues/1099
-->
<script lang="ts">
  import { createEventDispatcher, tick } from 'svelte';
  import { Dropdown } from '@mathesar-component-library';
  import BaseInput from '@mathesar-component-library-dir/common/base-components/BaseInput.svelte';
  import type { Appearance } from '@mathesar-component-library/types';
  import type { SelectOption } from './Select.d';

  const dispatch = createEventDispatcher();

  export let id: string | undefined = undefined;

  export let disabled = false;

  // DISCUSS: Maybe valueKey = 'value' is a better term to use than idKey
  /**
   * Specifies the key on which the options ID is stored.
   */
  export let idKey = 'id';

  /**
   * Specifies the key on which the options label is stored.
   */
  export let labelKey = 'label';

  /**
   * List of options to select from. Must be an array of SelectOption.
   * @required
   */
  export let options: SelectOption[] = [];

  /**
   * Currently selected option.
   *
   * TODO: convert this to use undefined instead of null or explain why we're
   * using null here.
   */
  export let value: SelectOption | null = null;

  /**
   * Classes to apply to the content (each of the options).
   */
  export let contentClass = '';

  /**
   * Classes to apply to the trigger button (the dropdown button).
   */
  export let triggerClass = '';

  /**
   * Appearance of the trigger button. One of: 'default', 'primary', 'secondary', 'plain', 'ghost'.
   */
  export let triggerAppearance: Appearance = 'plain';

  /**
   * The ARIA label for this select component.
   */
  export let ariaLabel: string | undefined = undefined;

  let isOpen = false;
  let currentIndex = 0;
  let parentHoverElem: HTMLElement;

  function setValue(opt: SelectOption | null) {
    value = opt;
    dispatch('change', {
      value, // TODO: Change this to reflect value within option
      option: value,
    });
    isOpen = false;
  }

  function setOptions(opts: SelectOption[]) {
    if (opts.length > 0) {
      if (!value) {
        setValue(opts[0]);
      } else if (
        !opts.find((entry) => value && entry[idKey] === value[idKey])
      ) {
        setValue(opts[0]);
      }
    } else {
      setValue(null);
    }
  }

  function scrollBehavior(): void {
    if (parentHoverElem) {
      const hoveredElem: HTMLElement | null =
        parentHoverElem.querySelector('.hovered');
      const container = parentHoverElem.parentElement as HTMLDivElement;
      if (hoveredElem && container) {
        if (
          hoveredElem.offsetTop + hoveredElem.clientHeight >
          container.scrollTop + container.clientHeight
        ) {
          const offsetValue: number =
            container.getBoundingClientRect().bottom -
            hoveredElem.getBoundingClientRect().bottom;
          container.scrollTop -= offsetValue;
        } else if (hoveredElem.offsetTop < container.scrollTop) {
          container.scrollTop = hoveredElem.offsetTop;
        }
      }
    }
  }

  function setSelectedItem() {
    const index = options.findIndex((e) => e[idKey] === value?.[idKey]);
    if (index > -1) {
      currentIndex = index;
    }
  }

  async function hoveredItem(index: number): Promise<void> {
    if (currentIndex === options.length - 1 && index > 0) {
      currentIndex = 0;
    } else if (currentIndex === 0 && index < 0) {
      currentIndex = options.length - 1;
    } else {
      currentIndex += index;
    }
    await tick();
    scrollBehavior();
  }

  function keyAccessibility(e: KeyboardEvent): void {
    if (isOpen) {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          void hoveredItem(1);
          break;
        case 'ArrowUp':
          e.preventDefault();
          void hoveredItem(-1);
          break;
        case 'Escape':
          e.preventDefault();
          isOpen = false;
          break;
        case 'Enter':
          e.preventDefault();
          if (options.length === 0) break;
          value = options[currentIndex];
          dispatch('change', {
            value,
          });
          isOpen = !isOpen;
          break;
        default:
          break;
      }
    } else {
      switch (e.key) {
        case 'Enter':
        case 'ArrowDown':
        case 'ArrowUp':
          e.preventDefault();
          isOpen = true;
          break;
        default:
          break;
      }
    }
  }

  $: setOptions(options);
</script>

<BaseInput {...$$restProps} bind:id {disabled} />

<Dropdown
  ariaControls="{id}-select-options"
  {ariaLabel}
  bind:isOpen
  {disabled}
  {id}
  contentClass="select {contentClass}"
  {triggerAppearance}
  {triggerClass}
  on:keydown={keyAccessibility}
  on:open={setSelectedItem}
>
  <svelte:fragment slot="trigger">
    {value?.[labelKey]}
  </svelte:fragment>

  <svelte:fragment slot="content">
    <ul
      bind:this={parentHoverElem}
      id="{id}-select-options"
      tabindex="0"
      role="listbox"
      aria-expanded="true"
    >
      {#each options as option (option[idKey])}
        <li
          role="option"
          class:selected={value && option[idKey] === value[idKey]}
          class:hovered={option[idKey] === options[currentIndex]?.[idKey]}
          on:click={() => setValue(option)}
        >
          <span>{option[labelKey]}</span>
        </li>
      {/each}
    </ul>
  </svelte:fragment>
</Dropdown>
