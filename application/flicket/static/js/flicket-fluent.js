(function () {
    'use strict';

    var root = document.documentElement;
    var THEME_KEY = 'flicket-theme';
    var apiBase = document.body.getAttribute('data-api-base') || '/flicket-api/';
    var MIN_SEARCH_LENGTH = 3;

    function setTheme(theme) {
        root.setAttribute('data-theme', theme);
        try {
            localStorage.setItem(THEME_KEY, theme);
        } catch (e) {
        }
    }

    document.addEventListener('click', function (event) {
        var target = event.target;
        var control;

        if ((control = target.closest('[data-theme-toggle]'))) {
            setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
        } else if ((control = target.closest('[data-drawer-open]'))) {
            document.getElementById(control.getAttribute('data-drawer-open')).show();
        } else if ((control = target.closest('[data-drawer-close]'))) {
            document.getElementById(control.getAttribute('data-drawer-close')).hide();
        } else if ((control = target.closest('[data-dismiss-message]'))) {
            control.closest('fluent-message-bar').remove();
        }
    });

    function apiGet(path, params) {
        var headers = {};
        var meta = document.querySelector('meta[name="flicket-api-token"]');
        var query = params ? '?' + new URLSearchParams(params).toString() : '';

        if (meta && meta.content) {
            headers.Authorization = 'Bearer ' + meta.content;
        }

        return fetch(apiBase + path + query, {headers: headers, credentials: 'same-origin'}).then(function (response) {
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.json();
        });
    }

    function initCombobox(wrapper) {
        var input = wrapper.querySelector('input');
        var listbox = wrapper.querySelector('[role="listbox"]');
        var timer = null;
        var lastRequest = 0;
        var options = [];
        var active = -1;

        function setActive(index) {
            active = index;
            options.forEach(function (option, i) {
                var current = i === index;
                option.classList.toggle('is-active', current);
                option.setAttribute('aria-selected', current ? 'true' : 'false');
            });
            if (index >= 0) {
                input.setAttribute('aria-activedescendant', options[index].id);
            } else {
                input.removeAttribute('aria-activedescendant');
            }
        }

        function setOpen(open) {
            listbox.hidden = !open;
            input.setAttribute('aria-expanded', open ? 'true' : 'false');
            if (!open) {
                setActive(-1);
            }
        }

        function choose(index) {
            if (index < 0 || !options[index]) {
                return;
            }
            input.value = options[index].getAttribute('data-value');
            setOpen(false);
        }

        function render(items) {
            listbox.textContent = '';
            options = items.map(function (item, index) {
                var option = document.createElement('li');
                option.id = input.id + '-option-' + index;
                option.className = 'fl-combobox__option';
                option.setAttribute('role', 'option');
                option.setAttribute('aria-selected', 'false');
                option.setAttribute('data-value', item.username);
                option.textContent = item.name + ' (' + item.username + ')';
                option.addEventListener('mousedown', function (event) {
                    event.preventDefault();
                    choose(index);
                });
                listbox.appendChild(option);
                return option;
            });
            setActive(-1);
            setOpen(options.length > 0 && document.activeElement === input);
        }

        function search() {
            var term = input.value.trim();
            var request = ++lastRequest;

            if (term.length < MIN_SEARCH_LENGTH) {
                render([]);
                return;
            }

            apiGet('users/', {name: term}).then(function (data) {
                if (request === lastRequest) {
                    render(data.items || []);
                }
            }).catch(function () {
                if (request === lastRequest) {
                    render([]);
                }
            });
        }

        input.addEventListener('input', function () {
            clearTimeout(timer);
            timer = setTimeout(search, 250);
        });

        input.addEventListener('keydown', function (event) {
            var count = options.length;
            var next;

            if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                if (!count) {
                    return;
                }
                event.preventDefault();
                setOpen(true);
                if (active < 0) {
                    next = event.key === 'ArrowDown' ? 0 : count - 1;
                } else {
                    next = (active + (event.key === 'ArrowDown' ? 1 : -1) + count) % count;
                }
                setActive(next);
                options[next].scrollIntoView({block: 'nearest'});
            } else if (event.key === 'Enter') {
                if (!listbox.hidden && active >= 0) {
                    event.preventDefault();
                    choose(active);
                }
            } else if (event.key === 'Escape') {
                if (!listbox.hidden) {
                    event.preventDefault();
                    setOpen(false);
                }
            }
        });

        input.addEventListener('blur', function () {
            setOpen(false);
        });
    }

    function initDependentCategories() {
        var department = document.getElementById('department');
        var category = document.getElementById('category');
        var placeholder;

        if (!department || !category) {
            return;
        }

        placeholder = category.getAttribute('data-placeholder') || '';

        function fill(items, selected) {
            var listbox = category.querySelector('fluent-listbox');
            listbox.textContent = '';
            items.forEach(function (item) {
                var option = document.createElement('fluent-option');
                option.setAttribute('name', category.getAttribute('name'));
                option.setAttribute('value', item.value);
                option.setAttribute('text', item.text);
                option.textContent = item.text;
                if (item.value === selected) {
                    option.setAttribute('selected', '');
                }
                listbox.appendChild(option);
            });
            window.setTimeout(function () {
                category.value = selected;
            }, 0);
        }

        function load(keepSelected) {
            var departmentId = department.value;
            var selected = keepSelected ? category.value : '0';

            if (!departmentId || departmentId === '0') {
                fill([{value: '0', text: placeholder}], '0');
                return;
            }

            apiGet('categories/', {department_id: departmentId}).then(function (data) {
                var items = [{value: '0', text: placeholder}];
                (data.items || []).forEach(function (item) {
                    items.push({value: String(item.id), text: item.category});
                });
                var keep = items.some(function (item) {
                    return item.value === selected;
                });
                fill(items, keep ? selected : '0');
            }).catch(function () {
            });
        }

        department.addEventListener('change', function () {
            load(false);
        });
        load(true);
    }

    function applyInitialDropdownValues() {
        document.querySelectorAll('fluent-dropdown[value]').forEach(function (dropdown) {
            var initial = dropdown.getAttribute('value');
            if (initial && dropdown.value !== initial) {
                window.setTimeout(function () {
                    dropdown.value = initial;
                }, 0);
            }
        });
    }

    function initMenuLinks() {
        document.querySelectorAll('fluent-menu-item').forEach(function (item) {
            var link = item.querySelector('a[href]');
            if (!link) {
                return;
            }
            item.addEventListener('click', function (event) {
                if (event.defaultPrevented) {
                    window.location.assign(link.href);
                }
            });
            item.addEventListener('keydown', function (event) {
                if (event.key === 'Enter') {
                    window.location.assign(link.href);
                }
            });
        });
    }

    applyInitialDropdownValues();
    initMenuLinks();
    document.querySelectorAll('[data-combobox]').forEach(initCombobox);
    initDependentCategories();
})();
