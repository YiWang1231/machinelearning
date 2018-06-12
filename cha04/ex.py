#coding:utf-8
__author__ = 'Yi'
__date__ = '08/06/2018 7:51 PM'

from numpy import *

# class Solution:
#     def NumberOf1(self, n):
#         # write code here
#         return sum([(n>>i&1) for i in range(0,32)])
#
# class Solution:
#     def Power(self, base, exponent):
#         flag = 0
#         if base == 0:
#             return False
#         if exponent == 0:
#             return 1
#         if exponent < 0:
#             flag = 1
#         result = 1
#         for i in range(abs(exponent)):
#             result *= base
#         if flag == 1:
#             return 1 / result
#         return result

# class Solution:
#     def FindKthToTail(self, head, k):
#             # write code here
#             list = []
#             list.append(head)
#             while head:
#                 list.insert(0, head)
#                 head = head.next
#             if (len(list) < k) or (k < 1):
#                 return
#             return list[k-1]


class Solution:
    # 返回ListNode
    def ReverseList(self, pHead):
        # write code here
        if (pHead is None) | (pHead.next is None):
            return
        head = pHead
        temp_next = None
        while head:
            if head.next:
                next_head = head.next
                head.next = temp_next
                temp_next = head
                head = next_head
            else:
                head.next = temp_next
                break
        list = []
        while head:
            list.append(head.val)
            head = head.next
        return list



class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    node1 = ListNode(a[0])
    node2 = ListNode(a[1])
    node3 = ListNode(a[2])
    node4 = ListNode(a[3])
    node5 = ListNode(a[4])
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5

    print(node2.next.next)
    s = Solution()
    b = s.ReverseList(node1)
    print(b)
    print(list(range(50))[5])