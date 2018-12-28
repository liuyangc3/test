/**
 * Original from vs code vs/base/common/map.ts
 */
export class TernarySearchTree<E> {
    private _iter: IKeyIterator;
    private _root: TreeNode<E>;

    static forStrings<E>(): TernarySearchTree<E> {
        return new TernarySearchTree<E>(new StringIterator());
    }

    constructor(segments: IKeyIterator) {
        this._iter = segments;
    }

    clear(): void {
        this._root = undefined;
    }

    set(key: string, element: E): E {
        const iter = this._iter.reset(key);

        let node: TreeNode<E>;
        if (!this._root) {
            this._root = new TreeNode<E>();
            this._root.str = iter.value();
        }

        node = this._root;
        while (true) {
            const val = iter.cmp(node.str);
            if (val > 0) {
                // left
                if (!node.left) {
                    node.left = new TreeNode<E>();
                    node.left.str = iter.value();
                }
                node = node.left;
            } else if (val < 0) {
                // right
                if (!node.right) {
                    node.right = new TreeNode<E>();
                    node.right.str = iter.value();
                }
                node = node.right;
            } else if (iter.hasNext()) {
                // mid
                iter.next();
                if (!node.mid) {
                    node.mid = new TreeNode<E>();
                    node.mid.str = iter.value();
                }
                node = node.mid;
            } else {
                break;
            }
        }

        const oldElement = node.element;
        node.element = element;
        return oldElement;
    }

    get(key: string): E {
        const iter = this._iter.reset(key);
        let node = this._root;
        while (node) {
            const val = iter.cmp(node.str);
            if (val > 0) {
                // left
                node = node.left;
            } else if (val < 0) {
                // right
                node = node.right;
            } else if (iter.hasNext()) {
                // mid
                iter.next();
                node = node.mid;
            } else {
                break;
            }
        }
        return node ? node.element : undefined;
    }

    delete(key: string): void {

        const iter = this._iter.reset(key);
        const stack: [-1 | 0 | 1, TreeNode<E>][] = [];
        let node = this._root;

        // find and unset node
        while (node) {
            const val = iter.cmp(node.str);
            if (val > 0) {
                // left
                stack.push([1, node]);
                node = node.left;
            } else if (val < 0) {
                // right
                stack.push([-1, node]);
                node = node.right;
            } else if (iter.hasNext()) {
                // mid
                iter.next();
                stack.push([0, node]);
                node = node.mid;
            } else {
                // remove element
                node.element = undefined;

                // clean up empty nodes
                while (stack.length > 0 && node.isEmpty()) {
                    const [dir, parent] = stack.pop();
                    switch (dir) {
                        case 1: parent.left = undefined; break;
                        case 0: parent.mid = undefined; break;
                        case -1: parent.right = undefined; break;
                    }
                    node = parent;
                }
                break;
            }
        }
    }

    findSuperstr(key: string): TernarySearchTree<E> {
        const iter = this._iter.reset(key);
        let node = this._root;
        while (node) {
            const val = iter.cmp(node.str);
            if (val > 0) {
                // left
                node = node.left;
            } else if (val < 0) {
                // right
                node = node.right;
            } else if (iter.hasNext()) {
                // mid
                iter.next();
                node = node.mid;
            } else {
                // collect
                if (!node.mid) {
                    return undefined;
                }
                const ret = new TernarySearchTree<E>(this._iter);
                ret._root = node.mid;
                return ret;
            }
        }
        return undefined;
    }

    *generator() {
        const stack: TreeNode<E>[] = [];
        stack.push(this._root);

        while (stack.length > 0) {
            let node: TreeNode<E> = stack.pop();
            if (node.element) {
                yield node.element;
            }

            if (node.left) { stack.push(node.left); }
            if (node.mid) { stack.push(node.mid); }
            if (node.right) { stack.push(node.right); }
        }
    }

    forEach(callback: (value: E, index: string) => any) {
        this._forEach(this._root, [], callback);
    }

    private _forEach(node: TreeNode<E>, parts: string[], callback: (value: E, index: string) => any) {
        if (node) {
            // left
            this._forEach(node.left, parts, callback);

            // node
            parts.push(node.str);
            if (node.element) {
                callback(node.element, this._iter.join(parts));
            }
            // mid
            this._forEach(node.mid, parts, callback);
            parts.pop();

            // right
            this._forEach(node.right, parts, callback);
        }
    }
}

class TreeNode<E> {
    str: string;
    element: E;
    left: TreeNode<E>;
    mid: TreeNode<E>;
    right: TreeNode<E>;

    isEmpty(): boolean {
        return !this.left && !this.mid && !this.right && !this.element;
    }
}

interface IKeyIterator {
    reset(key: string): this;
    next(): this;
    join(parts: string[]): string;

    hasNext(): boolean;
    cmp(a: string): number;
    value(): string;
}

class StringIterator implements IKeyIterator {

    private _value = '';
    private _pos = 0;

    reset(key: string): this {
        this._value = key;
        this._pos = 0;
        return this;
    }

    next(): this {
        this._pos += 1;
        return this;
    }

    join(parts: string[]): string {
        return parts.join('');
    }

    hasNext(): boolean {
        return this._pos < this._value.length - 1;
    }

    cmp(a: string): number {
        const aCode = a.charCodeAt(0);
        const thisCode = this._value.charCodeAt(this._pos);
        return aCode - thisCode;
    }

    value(): string {
        return this._value[this._pos];
    }
