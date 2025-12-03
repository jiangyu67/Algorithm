class TreeNode:
    """增强版BST节点类"""

    def __init__(self, val):
        self.val = val
        self.left = None  # 左子节点
        self.right = None  # 右子节点
        self.count = 1  # 节点值的重复计数（处理重复值）
        self.size = 1  # 以当前节点为根的子树节点总数（含重复）

    def update_size(self):
        """更新当前节点的子树大小"""
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        self.size = left_size + right_size + self.count

    def get_height(self):
        """计算当前节点的高度（空节点高度为-1）"""
        if not self:
            return -1
        left_height = self.left.get_height() if self.left else -1
        right_height = self.right.get_height() if self.right else -1
        return 1 + max(left_height, right_height)


class EnhancedBST:
    """增强版BST类"""

    def __init__(self):
        self.root = None

    # ------------------- 基础功能：插入 -------------------
    def insert(self, val):
        """插入值（支持重复值）"""
        self.root = self._insert_recursive(self.root, val)

    def _insert_recursive(self, node, val):
        if not node:
            return TreeNode(val)

        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        else:
            # 重复值：增加计数
            node.count += 1

        # 插入后更新子树大小
        node.update_size()
        return node

    # ------------------- 基础功能：删除 -------------------
    def delete(self, val):
        """删除值（支持删除重复值，全部删除）"""
        self.root = self._delete_recursive(self.root, val)

    def _delete_recursive(self, node, val):
        if not node:
            return None

        # 1. 查找待删除节点
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # 2. 处理删除逻辑
            # 场景1：重复值，先减少计数
            if node.count > 1:
                node.count -= 1
                node.update_size()
                return node
            # 场景2：叶子节点
            if not node.left and not node.right:
                return None
            # 场景3：仅单个子树
            elif not node.left:
                return node.right
            elif not node.right:
                return node.left
            # 场景4：两个子树（找中序后继替换）
            else:
                # 找右子树最小节点（中序后继）
                min_right = node.right
                while min_right.left:
                    min_right = min_right.left
                # 替换值+计数
                node.val = min_right.val
                node.count = min_right.count
                # 删除后继节点（先置空计数，避免重复删除）
                min_right.count = 1
                node.right = self._delete_recursive(node.right, min_right.val)

        # 删除后更新子树大小
        node.update_size()
        return node

    # ------------------- 基础功能：查找 -------------------
    def search(self, val):
        """查找值，返回节点（None表示不存在）"""
        return self._search_recursive(self.root, val)

    def _search_recursive(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search_recursive(node.left, val)
        return self._search_recursive(node.right, val)

    # ------------------- 增强功能：前驱/后继 -------------------
    def find_predecessor(self, val):
        """查找val的前驱（小于val的最大值）"""
        predecessor = None
        current = self.root
        while current:
            if current.val < val:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor.val if predecessor else None

    def find_successor(self, val):
        """查找val的后继（大于val的最小值）"""
        successor = None
        current = self.root
        while current:
            if current.val > val:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor.val if successor else None

    # ------------------- 增强功能：范围查询 -------------------
    def range_query(self, low, high):
        """查找[low, high]区间内的所有值（升序）"""
        result = []
        self._range_query_recursive(self.root, low, high, result)
        return result

    def _range_query_recursive(self, node, low, high, result):
        if not node:
            return
        if node.val > low:
            self._range_query_recursive(node.left, low, high, result)
        if low <= node.val <= high:
            # 重复值需多次添加
            result.extend([node.val] * node.count)
        if node.val < high:
            self._range_query_recursive(node.right, low, high, result)

    # ------------------- 增强功能：统计与验证 -------------------
    def get_tree_size(self):
        """获取整树节点总数（含重复）"""
        return self.root.size if self.root else 0

    def get_tree_height(self):
        """获取整树高度"""
        return self.root.get_height() if self.root else -1

    def is_valid_bst(self):
        """验证当前树是否为合法BST"""
        return self._is_valid_recursive(self.root, float('-inf'), float('inf'))

    def _is_valid_recursive(self, node, min_val, max_val):
        if not node:
            return True
        if node.val <= min_val or node.val >= max_val:
            return False
        return (self._is_valid_recursive(node.left, min_val, node.val) and
                self._is_valid_recursive(node.right, node.val, max_val))

    # ------------------- 增强功能：遍历 -------------------
    def pre_order(self):
        """前序遍历：根→左→右"""
        result = []
        self._pre_order_recursive(self.root, result)
        return result

    def in_order(self):
        """中序遍历：左→根→右（BST中序为升序）"""
        result = []
        self._in_order_recursive(self.root, result)
        return result

    def post_order(self):
        """后序遍历：左→右→根"""
        result = []
        self._post_order_recursive(self.root, result)
        return result

    def level_order(self):
        """层序遍历（广度优先）"""
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.extend([node.val] * node.count)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def _pre_order_recursive(self, node, result):
        if not node:
            return
        result.extend([node.val] * node.count)
        self._pre_order_recursive(node.left, result)
        self._pre_order_recursive(node.right, result)

    def _in_order_recursive(self, node, result):
        if not node:
            return
        self._in_order_recursive(node.left, result)
        result.extend([node.val] * node.count)
        self._in_order_recursive(node.right, result)

    def _post_order_recursive(self, node, result):
        if not node:
            return
        self._post_order_recursive(node.left, result)
        self._post_order_recursive(node.right, result)
        result.extend([node.val] * node.count)

    # ------------------- 增强功能：清空树 -------------------
    def clear(self):
        """清空整树（释放所有节点）"""
        self.root = None


