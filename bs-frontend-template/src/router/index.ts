import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import { IMenubarList } from '/@/type/store/layout'
import { components } from '/@/router/asyncRouter'

const Components: IObject<() => Promise<typeof import('*.vue')>> = Object.assign({}, components, {
    Layout: (() => import('/@/layout/index.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    Redirect: (() => import('/@/layout/redirect.vue')) as unknown as () => Promise<typeof import('*.vue')>,
    LayoutBlank: (() => import('/@/layout/blank.vue')) as unknown as () => Promise<typeof import('*.vue')>
})

// 静态路由页面
export const allowRouter: Array<IMenubarList> = [
    {
        name: 'Data',
        path: '/',
        component: Components['Layout'],
        redirect: '/Data/List',
        meta: { title: '租房信息', icon: '' },
        children: [
            {
                name: 'DataList',
                path: '/Data/List',
                component: Components['List'],
                meta: { title: '租房信息', icon: '' }
            }
        ]
    },
    {
        name: 'Charts',
        path: '/Charts',
        component: Components['Layout'],
        redirect: '/Charts/Index',
        meta: { title: '可视化分析', icon: '' },
        children: [
            {
                name: 'ChartsIndex',
                path: '/Charts/Index',
                component: Components['Charts'],
                meta: { title: '可视化分析', icon: '' }
            }
        ]
    },
    {
        name: 'Reserve',
        path: '/reserve',
        component: Components['Layout'],
        redirect: '/Reserve/Index',
        meta: { title: '房屋预定', icon: '' },
        children: [
            {
                name: 'ReserveIndex',
                path: '/Reserve/Index',
                component: Components['Reserve'],
                meta: { title: '房屋预定', icon: '' }
            }
        ]
    },
    {
        name: 'Detail_',
        path: '/Detail',
        component: Components['Layout'],
        meta: { title: '租房详情', icon: '', hidden: true },
        children: [
            {
                name: 'Detail',
                path: '/Detail/:id',
                props: true,
                component: Components['Detail'],
                meta: { title: '租房详情', icon: '' }
            }
        ]
    },
    {
        name: 'ErrorPage',
        path: '/ErrorPage',
        meta: { title: '错误页面', icon: 'el-icon-eleme', hidden: true },
        component: Components.Layout,
        redirect: '/ErrorPage/404',
        children: [
            {
                name: '401',
                path: '/ErrorPage/401',
                component: Components['401'],
                meta: { title: '401', icon: 'el-icon-s-tools' }
            },
            {
                name: '404',
                path: '/ErrorPage/404',
                component: Components['404'],
                meta: { title: '404', icon: 'el-icon-s-tools' }
            }
        ]
    },
    {
        name: 'RedirectPage',
        path: '/redirect',
        component: Components['Layout'],
        meta: { title: '重定向页面', icon: 'el-icon-eleme', hidden: true },
        children: [
            {
                name: 'Redirect',
                path: '/redirect/:pathMatch(.*)*',
                meta: {
                    title: '重定向页面',
                    icon: ''
                },
                component: Components.Redirect
            }
        ]
    },
    {
        name: 'Login',
        path: '/Login',
        component: Components.Login,
        meta: { title: '登录', icon: 'el-icon-eleme', hidden: true }
    },
    {
        name: 'Register',
        path: '/Register',
        component: Components.Register,
        meta: { title: '注册', icon: 'el-icon-eleme', hidden: true }
    },
]

const router = createRouter({
    history: createWebHashHistory(), // createWebHistory
    routes: allowRouter as RouteRecordRaw[]
})

export default router