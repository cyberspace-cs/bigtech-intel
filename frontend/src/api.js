// 后端 API 封装：开发走 Vite 代理（/api -> :8031），生产走同源挂载。
const BASE = '/api'

async function request(method, path, body, params) {
  let url = BASE + path
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== '' && v !== undefined && v !== null)
    ).toString()
    if (qs) url += '?' + qs
  }
  const opt = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body) opt.body = JSON.stringify(body)
  const res = await fetch(url, opt)
  if (!res.ok) throw new Error(`请求失败 ${res.status}`)
  return res.json()
}

export const api = {
  companies: (q = '', tier = 0) => request('GET', '/companies', null, { q, tier }),
  lineage: () => request('GET', '/lineage'),
  resumeTips: () => request('GET', '/resume/tips'),
  resumeStrategy: () => request('GET', '/resume/strategy'),
  recruit: (tier = 0) => request('GET', '/recruit', null, { tier }),
  jdList: (tier = 0, jtype = 0, q = '') => request('GET', '/jd', null, { tier, jtype, q }),
  jdParse: (payload) => request('POST', '/jd/parse', payload),
  jdAdd: (payload) => request('POST', '/jd', payload),
  jdDelete: (jid) => request('DELETE', `/jd/${jid}`),
  crawlTrigger: (payload) => request('POST', '/crawl/trigger', payload),
  crawlLogs: () => request('GET', '/crawl/logs'),
  crawlFacts: (companyId) =>
    request('GET', '/crawl/facts', null, { company_id: companyId || '' }),
}
